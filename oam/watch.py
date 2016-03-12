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
import version

"""
"""
class Watch(object):

    ROW1_HEIGHT = '9'
    ROW2_HEIGHT = '9'

    COL1_WIDTH = '45'
    COL2_WIDTH = '40'

    HOSTNAME = os.uname()[1]
    KERNEL_VER = os.uname()[2]

    def __init__(self, row1, row2, col1, col2):
        self.row1 = row1
        self.row2 = row2
        self.col1 = col1
        self.col2 = col2
        self.watch_dir = self.lastdate()

    def title(self):
        return self.HOSTNAME + '/oam/' + self.watch_dir + '/' + \
            self.KERNEL_VER + ' gentoo-oam V' + version.__version__

    def lastdate(self):
        datedir = glob.glob(os.getenv('OAM_LOGDIR', '/var/log/oam') + '/2*')
        if len(datedir)>1:
            return datedir[-1]
        else:
            return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')

    def make_conf(self):
        if os.path.exists('/etc/make.conf'):
            return '/etc/make.conf'
        elif os.path.exists('/etc/portage/make.conf'):
            return '/etc/portage/make.conf'

    def run(self):
        cmd = [ 'multitail',
                '-x', self.title(),
                '--config', '/usr/share/gentoo-oam/gentoo-oam-multitail.conf',
                '--basename',
                '-sw', self.col1 + ',' + self.col2, # widths of each column
                '-sn', '3,4',                       # window count per column

                '-wh', self.row1, '/usr/share/gentoo-oam/oam-watch.help', # win1: help
                '--retry',
                '-wh', self.row2, self.watch_dir + '/oam.log',            # win2: oam activity log
                '-j',                                                     # win3: stdin - genlop piped

                '-wh', self.row1, '-l', 'oam emergelog',                  # win4: /var/log/emerge.log
                '--retry-all',
                '-wh', self.row2, self.watch_dir + '/error.log',          # win5: general error log

                '--mark-change', '-T',

                '-i', self.watch_dir + '/sync.log',                       # win6: misc logs
                '-I', self.watch_dir + '/merge.log',
                '--label', 'blocks ', '-I', self.watch_dir + '/blocks.log',
                '-t', 'sync/merge/blocks/kernel ',
                '-I', self.watch_dir + '/kernel.log',
                '-I', self.watch_dir + '/summary.log'# ,
                # os.getenv('OAM_MULTITAIL_EXTRA_OPT', '')
        ]
        #subprocess.call(cmd)
        genlop = subprocess.Popen(['oam', 'genlop'], stdout=subprocess.PIPE)
        multitail = subprocess.Popen(cmd, stdin=genlop.stdout)
        return multitail.wait()

@cli.command()
@click.option('--row1', default=Watch.ROW1_HEIGHT, envvar='OAM_ROW1_HEIGHT')
@click.option('--row2', default=Watch.ROW2_HEIGHT, envvar='OAM_ROW2_HEIGHT')
@click.option('--col1', default=Watch.COL1_WIDTH, envvar='OAM_ROW1_HEIGHT')
@click.option('--col2', default=Watch.COL2_WIDTH, envvar='OAM_ROW2_HEIGHT')
def watch(row1, row2, col1, col2):
    """Dashboard overview of current system update"""
    return Watch(row1, row2, col1, col2).run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    sys.exit(Watch().run())
