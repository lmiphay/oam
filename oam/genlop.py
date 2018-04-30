# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import time
import logging
import pyinotify
import psutil
import click
from oam.cmd import cli
import oam.settings

EMERGE_LOG = '/var/log/emerge.log'

def timestamp():
    return time.strftime('%Y-%m-%d:%H:%M:%S')

def run(cmd):
    return os.popen(cmd).read()

def strip_version(atom):
    """sed courtesy think4urs11 @ https://forums.gentoo.org/viewtopic-p-5114319.html#5114319"""
    return run("echo " + atom + "|sed 's/-[0-9]\{1,\}.*$//'").strip()

class Genlop(object):

    """
    20160227:20:16:41 33/33 pkgs
      www-client/chromium-48.0.2564.116
      Gone: 5 hrs, 49 min 19 sec
      Left: 7 hrs, 41 min 48 sec
    """
    CURRENT = "{timestamp:s} {num:s}/{total:s} pkgs\n  {pkg:s}\n  Gone: {gone:s}\n  Left: {left:s}"

    def __init__(self):
        self.logger = logging.getLogger("oam.genlop")
        self.nap = oam.settings.oam.heartbeatsleep
        self.sandboxwait = oam.settings.oam.sandboxwait

    def genlop_current(self):
        """
        Currently merging 4 out of 17

        * dev-libs/xapian-1.2.22

        current merge time: 10 seconds.
        ETA: less than a minute.
        --
        Currently merging 33 out of 33

        * www-client/chromium-48.0.2564.116

        current merge time: 5 hours, 52 minutes and 1 second.
        ETA: 7 hours, 39 minutes and 6 seconds.
        """
        info = run('genlop --nocolor --current').\
               replace('\n', '').\
               replace('minutes', 'min').\
               replace('seconds', 'sec').\
               replace('hour', 'hr').\
               replace(' and ', ' ').\
               split(' ')
        self.logger.log(logging.DEBUG, 'RAW GENLOP: %s', str(info))
        if len(info)<29 or info[1] != 'Currently' or 'ETA:' not in info:
            return None
        else:
            eta = info.index('ETA:')
            return {'timestamp': timestamp(),
                    'num':info[3], 'total':info[6], 'pkg':info[8], 'gone':' '.join(info[19:eta]), 'left':' '.join(info[eta+1:])}

    def wait_for_sandbox(self, wait_time):
        """Wait for sandbox process to appear - genlop bales without it"""
        for t in xrange(int(wait_time)):
            for proc in psutil.process_iter():
                if proc.name() == 'sandbox':
                    return True
            time.sleep(1.0)
        return False

    def log_current(self):
        data = self.genlop_current()
        if data != None:
            print(self.CURRENT.format(**data))
            sys.stdout.flush()

    def log_currentcompile(self, wait_time):
        if self.wait_for_sandbox(wait_time):
            self.log_current()

    def notify(self):
        self.log_currentcompile(self.sandboxwait)


class Heartbeat(object):

    HEARTBEAT = "{timestamp:s} {uptime[0]:4.2f} {uptime[1]:4.2f} {uptime[2]:4.2f} {df[0]:.0%} {df[1]:.0%}"

    def __init__(self):
        self.logger = logging.getLogger("oam.heartbeat")
        self.monitor_count = 0
        self.hb = {}
        self.portage_tmpdir = self.tmpdir()

    def emerge_var(self, var):
        return run('emerge --verbose --info | egrep ^' + var + '=').strip().split('=')[1].replace('"', '')

    def tmpdir(self):
        return self.emerge_var('PORTAGE_TMPDIR')

    def disk_used(self, path):
        p = os.statvfs(path)
        space_percent = (p.f_blocks - p.f_bfree) / float(p.f_blocks)
        if p.f_files>0:
            inode_percent = (p.f_files - p.f_ffree) / float(p.f_files)
        else:
            inode_percent = 0.0
        return (space_percent, inode_percent)

    def notify(self):
        """
        Log some usage info regularly to show we are still alive
                               uptimes        df inode
             20150721:18:23:40 0.04 0.14 0.31 13% 1%   x
        """
        if self.monitor_count == 0:
            print("                    uptimes        df  inode")
        self.monitor_count += 1
        if self.monitor_count == 10:
            self.monitor_count = 0

        self.hb = {'timestamp': timestamp(), 'uptime': os.getloadavg(), 'df': self.disk_used(self.portage_tmpdir) }
        print(self.HEARTBEAT.format(**self.hb))
        sys.stdout.flush()


class Qlop(object):
    """Report on the currently running emerge useing qlop (q) from
       app-portage/portage-utils
    """

    CURRENT = 'qlop --current --nocolor'
    CURRENT_FORMAT = 'qlop: {atom} {started} elapsed={elapsed}'

    AVERAGE = 'qlop --time --nocolor {atom}'
    AVERAGE_FORMAT = 'qlop: {atom} {average} {merges}'

    GUAGE = 'qlop --gauge --nocolor {atom}'
    GUAGE_FORMAT = 'qlop: {atom} {started} elapsed={elapsed}'

    def __init__(self):
        self.logger = logging.getLogger("oam.qlop")
        self.last_modtime = -1
        self.averages = {}

    def average(self, atom):
        """oam: 18 seconds average for 9 merges"""
        if not atom in self.averages:
            output = run(self.AVERAGE.format(atom=atom)).split(': ')[1].split(' average for ')
            self.averages[atom] = {
                'atom': atom,
                'average': output[0],
                'merges': output[1].split()[1]
            }
        return self.averages[atom]

    def parse_current(self, info):
        """
       For the currently running query, the output is either empty or
       contains:
 * app-oam/oam-9999
     started: Thu Mar  8 16:01:54 2018
     elapsed: 2 seconds
        """
        return {
            'atom': strip_version(info[0].split()[1]),
            'package': info[0].split()[1],
            'started': info[1].split('started: ')[1],
            'elapsed': info[2].split('elapsed: ')
        }

    def notify(self):
        last_modtime = os.path.getmtime(EMERGE_LOG)
        if last_modtime > self.last_modtime:
            self.last_modtime = last_modtime
            output = run(self.CURRENT)
            if len(output) > 0:
                info = self.parse_current(output.splitlines())
                print(self.CURRENT_FORMAT.format(**info))
                print(self.AVERAGE_FORMAT.format(self.average(info['atom'])))
                sys.stdout.flush()


class Tail(pyinotify.ProcessEvent):

    def my_init(self, **kargs):
        #super().__init(self)
        self.wm = pyinotify.WatchManager()
        self.wdd = self.wm.add_watch(kargs['filename'], pyinotify.IN_MODIFY)
        self.watchers = kargs['watchers']
        self.heartbeat_every = kargs['heartbeat_every']

    def notify(self):
        for watcher in self.watchers:
            watcher.notify()

    def process_IN_MODIFY(self, event):
        #print("Modify:", event.pathname)
        self.notify()

    def event_loop(self):
        notifier = pyinotify.Notifier(self.wm, self, read_freq=100, timeout=self.heartbeat_every*1000)
        notifier.process_events()
        while True:
            self.notify()
            if notifier.check_events():
                """new events to read (are available)"""
                notifier.read_events()     # Read events, build _RawEvents, and enqueue them
                notifier.process_events()  # Process events from queue by calling their associated proccessing method


@cli.command()
def genlop():
    """Watch emerge.log for merge activity"""
    Tail(filename=EMERGE_LOG, watchers=[Heartbeat(), Genlop()], heartbeat_every=5).event_loop()

@cli.command()
def qlop():
    """Watch emerge.log for merge activity"""
    Tail(filename=EMERGE_LOG, watchers=[Heartbeat(), Qlop()], heartbeat_every=5).event_loop()
