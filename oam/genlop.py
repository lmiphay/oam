#!/usr/bin/python

from __future__ import print_function
import os
import sys
import time
import logging
import inotifyx
import psutil
import click
from .cmd import cli

class Genlop:

    HEARTBEAT = "{timestamp:s} {uptime[0]:4.2f} {uptime[1]:4.2f} {uptime[2]:4.2f} {df[0]:.1%} {df[1]:.1%}"

    """
    20160227:20:16:41 33/33 pkgs
      www-client/chromium-48.0.2564.116
      Gone: 5 hrs, 49 min 19 sec
      Left: 7 hrs, 41 min 48 sec
    """
    CURRENT = "{timestamp:s} {num:s}/{total:s} pkgs\n  {pkg:s}\n  Gone: {gone:s}\n  Left: {left:s}"

    def timestamp(self):
        return time.strftime('%Y-%m-%d:%H:%M:%S')

    def __init__(self):
        self.logger = logging.getLogger("oam.genlop")
        self.monitor_count = 0
        self.nap = os.getenv('OAM_HEARTBEATSLEEP', 5)
	self.sandboxwait = os.getenv('OAM_SANDBOXWAIT', 8)
        self.portage_tmpdir = self.tmpdir()
        self.hb = {}

    def run(self, cmd):
        return os.popen(cmd).read()

    def emerge_var(self, var):
        return self.run('emerge --verbose --info | egrep ^' + var + '=').strip().split('=')[1].replace('"', '')

    def tmpdir(self):
        return self.emerge_var('PORTAGE_TMPDIR')

    def disk_used(self, path):
        p = os.statvfs(path)
        space_percent = (p.f_blocks - p.f_bfree) / p.f_blocks
        if p.f_files>0:
            inode_percent = (p.f_files - p.f_ffree) / p.f_files
        else:
            inode_percent = 0
        return (space_percent, inode_percent)

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
        info = self.run('genlop --nocolor --current').\
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
            return {'timestamp': self.timestamp(),
                    'num':info[3], 'total':info[6], 'pkg':info[8], 'gone':' '.join(info[19:eta]), 'left':' '.join(info[eta+1:])}

    def wait_for_sandbox(self):
        """Wait for sandbox process to appear - genlop bales without it"""
        for t in xrange(int(self.sandboxwait)):
            for proc in psutil.process_iter():
                if proc.name() == 'sandbox':
                    return True
	    time.sleep(1.0)
        return False

    def log_current(self):
        data = self.genlop_current()
        if data != None:
            print(self.CURRENT.format(**data))

    def log_heartbeat(self):
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

        self.hb = {'timestamp': self.timestamp(), 'uptime': os.getloadavg(), 'df': self.disk_used(self.portage_tmpdir) }
        print(self.HEARTBEAT.format(**self.hb))

    def tail(self):
        fd = inotifyx.init()
        try:
            wd = inotifyx.add_watch(fd, '/var/log/emerge.log', inotifyx.IN_MODIFY)

            while True:
		self.log_heartbeat()
                events = inotifyx.get_events(fd, float(self.nap))
                if len(events) != 0: # not timeout
                    if self.wait_for_sandbox():
		        self.log_current()

            inotifyx.rm_watch(fd, wd)
        finally:
            os.close(fd)

@cli.command()
def genlop():
    """Watch emerge.log for merge activity"""
    Genlop().tail()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')

    sys.exit(Genlop().tail())
