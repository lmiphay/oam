#!/usr/bin/python

import sys
import os
import subprocess
import logging
import re
import click
from .cmd import cli
import glob
import time
import datetime
from version import get_version

ROW1_HEIGHT = '9'
ROW2_HEIGHT = '9'

COL1_WIDTH = '45'
COL2_WIDTH = '40'

def last_date():
    datedir = sorted(glob.glob(os.getenv('OAM_LOGDIR', '/var/log/oam') + '/2*'))
    if len(datedir) > 0:
        return datedir[-1]
    else:
        return None

"""
"""
class Watch(object):

    HOSTNAME = os.uname()[1]
    KERNEL_VER = os.uname()[2]

    def __init__(self, row1, row2, col1, col2):
        self.logger = logging.getLogger("oam.watch")
        self.row1 = row1
        self.row2 = row2
        self.col1 = col1
        self.col2 = col2
        self.watch_dir = last_date()

    def title(self):
        return "{}/oam/{}/{} gentoo-oam V{}".format(self.HOSTNAME, os.path.basename(self.watch_dir), self.KERNEL_VER, get_version())

    def make_conf(self):
        if os.path.exists('/etc/make.conf'):
            return '/etc/make.conf'
        elif os.path.exists('/etc/portage/make.conf'):
            return '/etc/portage/make.conf'
        else:
            return ""

    def run(self):
        os.chdir(self.watch_dir) # this makes the multitail command line a _lot_ shorter

        cmd = [ 'multitail',
                '-x', self.title(),
                '--config', '/usr/share/gentoo-oam/gentoo-oam-multitail.conf',
                '--basename',
                '-sw', self.col1 + ',' + self.col2, # widths of each column
                '-sn', '3,4',                       # window count per column

                '-wh', self.row1, '/usr/share/gentoo-oam/oam-watch.help', # win1: help
                '--retry',
                '-wh', self.row2, 'oam.log',                              # win2: oam activity log
                '-j',                                                     # win3: stdin - genlop piped

                '--retry',
                '-wh', self.row2, 'error.log',                            # win5: general error log
                '-wh', self.row1, '-l', 'oam emergelog',                  # win4: /var/log/emerge.log

                '--mark-change', '-T',

                '--retry-all',
                '-i', 'sync.log',                                         # win6: misc logs
                '-I', 'merge.log',
                '--label', 'blocks ', '-I', 'blocks.log',
                '-t', 'sync/merge/blocks/kernel ',                        # set title in statusline
                '-I', 'kernel.log',
                '-I', 'summary.log'
        ]

        extra_opt = os.getenv('OAM_MULTITAIL_EXTRA_OPT', None)
        if extra_opt:
            cmd.append(extra_opt)

        genlop = subprocess.Popen(['oam', 'genlop'], stdout=subprocess.PIPE)
        multitail = subprocess.Popen(cmd, stdin=genlop.stdout, env=dict(os.environ, OAM_MAKECONF=self.make_conf()))

        return multitail.wait()

@cli.command()
@click.option('--row1', default=ROW1_HEIGHT, envvar='OAM_ROW1_HEIGHT')
@click.option('--row2', default=ROW2_HEIGHT, envvar='OAM_ROW2_HEIGHT')
@click.option('--col1', default=COL1_WIDTH, envvar='OAM_ROW1_HEIGHT')
@click.option('--col2', default=COL2_WIDTH, envvar='OAM_ROW2_HEIGHT')
def watch(row1, row2, col1, col2):
    """Dashboard overview of current system update"""
    logdir = last_date()
    if logdir:
        return Watch(row1, row2, col1, col2).run()
    else:
        sys.exit("No log directory found")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    sys.exit(Watch().run())
