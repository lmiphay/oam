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

PERIOD = {
    'day': 3600*24,
    'hour': 3600,
    'minute': 60,
    'second': 1
}

def human_to_seconds(human):
    """return '1 days, 3 hours, 27 minutes, 30 seconds; in seconds"""
    human = human.replace(',', '').split()
    seconds = 0

    for period in PERIOD.keys():
        if period in human:
            seconds += PERIOD[period] * int(human[human.index(period)-1])
        elif period + 's' in human:
            seconds += PERIOD[period] * int(human[human.index(period + 's')-1])

    return seconds

class Qlop(object):
    """Report on the currently running emerge useing qlop (q) from
       app-portage/portage-utils
2018-05-06:16:16:13 3.09 3.09 3.12 73% 22%
www-client/chromium
 started Sun May  6 13:17:44 2018
 elapsed 10708
 average 87857 seconds in 33 merges
2018-05-06:16:16:18 3.08 3.09 3.11 73% 22%

2018-05-06 13:17:44 www-client/chromium
 20% (10708/182249 seconds, 33 merges)

kul ~ # qlop --gauge --nocolor www-client/chromium
chromium: Tue Aug  4 16:41:55 2015: 46778 seconds
chromium: Sun Aug 16 16:31:18 2015: 47292 seconds
...
chromium: Sat Feb 17 15:55:38 2018: 129289 seconds
chromium: Sat Mar 10 19:31:25 2018: 128681 seconds
chromium: Sun Apr  1 01:32:04 2018: 168672 seconds
chromium: Sun Apr 29 21:01:45 2018: 182249 seconds
chromium: 33 times
    """

    CURRENT = 'qlop --current --nocolor'
    CURRENT_FORMAT = '{atom}\n started {started}\n remain {remain}, elapsed {elapsed}/{last_merge}'

    AVERAGE = 'qlop --time --nocolor {atom}'
    AVERAGE_FORMAT = ' average {average} in {merges} merges'

    GAUGE = 'qlop --gauge --nocolor {atom} | tail -2 | head -1'

    def __init__(self):
        self.logger = logging.getLogger("oam.qlop")
        self.last_modtime = -1
        self.last_show = time.time()
        self.averages = {}
        self.last_merges = {}

    def last_merge(self, atom):
        """chromium: Sat May  5 11:31:46 2018: 13406 seconds"""
        if not atom in self.last_merges:
            output = run(self.GAUGE.format(atom=atom)).split(' ')
            if len(output)>2:
                self.last_merges[atom] = output[-2]
            else:
                self.last_merges[atom] = 'unknown'
        return self.last_merges[atom]

    def average(self, atom):
        """oam: 18 seconds average for 9 merges"""
        if not atom in self.averages:
            output = run(self.AVERAGE.format(atom=atom)).split(': ')[1].split(' average for ')
            self.averages[atom] = {
                'atom': atom,
                'average': output[0],
                'merges': output[1].split()[0]
            }
        return self.averages[atom]

    def remaining(self, elapsed_time, last_merge_time):
        if last_merge_time == 'unknown':
            return 'unknown'
        else:
            return int(last_merge_time) - int(elapsed_time)

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
            'elapsed': human_to_seconds(info[2].split('elapsed: ')[1]),
            'elapsed_human': info[2].split('elapsed: ')[1]
        }

    def show(self):
        output = ""  # run(self.CURRENT)
        if len(output) > 0:
            output = output.splitlines()
            if len(output) == 3:
                info = self.parse_current(output)
                print(self.CURRENT_FORMAT.format(last_merge=self.last_merge(info['atom']),
                                                 remain=self.remaining(info['elapsed'], self.last_merge(info['atom'])),
                                                 **info))
                print(self.AVERAGE_FORMAT.format(**self.average(info['atom'])))
                sys.stdout.flush()

    def notify(self):
        last_modtime = os.path.getmtime(EMERGE_LOG)
        if last_modtime > self.last_modtime:
            self.last_modtime = last_modtime
            self.last_show = time.time()
            self.show()
        elif time.time() > self.last_show + 120:
            self.last_show = time.time()
            self.show()

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

@cli.command()
def olop():
    """Summarise current emerge activity"""
    Qlop().show()

