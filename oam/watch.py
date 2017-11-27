# -*- coding: utf-8 -*-

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
from oam.version import get_version
import oam.settings
from oam.daylog import last_date

"""
"""
class Watch(object):

    HOSTNAME = os.uname()[1]
    KERNEL_VER = os.uname()[2]

    def __init__(self):
        self.logger = logging.getLogger("oam.watch")
        layout = oam.settings.multitail.layout
        self.row1 = str(layout.row1)
        self.row2 = str(layout.row2)
        self.col1 = str(layout.col1)
        self.col2 = str(layout.col2)
        self.watch_dir = last_date()

    def title(self):
        return "{}/oam/{}/{} oam V{}".format(self.HOSTNAME,
                                             os.path.basename(self.watch_dir),
                                             self.KERNEL_VER,
                                             get_version())

    def make_conf(self):
        if os.path.exists('/etc/make.conf'):
            return '/etc/make.conf'
        elif os.path.exists('/etc/portage/make.conf'):
            return '/etc/portage/make.conf'
        else:
            return ""

    def make_env(self):
        return dict(os.environ,
                    OAM_MAKECONF=self.make_conf()
        )

    def run(self):
        cmd = [ 'multitail',
                '-x', self.title(),
                '--config', '/usr/share/oam/oam-multitail.conf',
                '--basename',
                '-sw', self.col1 + ',' + self.col2, # widths of each column
                '-sn', '3,4',                       # window count per column

                '-wh', self.row1, '/usr/share/oam/oam-watch.help',        # win1: help
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
                '-I', 'summary.log',
                '-I', 'clean.log',
                '-I', 'misc.log',
                '-I', 'glsa.log',
                '-I', 'qcheck.log'
        ]

        extra_opt = oam.settings.multitail.extraopt
        if extra_opt:
            cmd.append(extra_opt)

        genlop = subprocess.Popen(['oam', 'genlop'], stdout=subprocess.PIPE, cwd=self.watch_dir)
        multitail = subprocess.Popen(cmd, stdin=genlop.stdout, env=self.make_env(), cwd=self.watch_dir)

        return multitail.wait()

@cli.command()
def watch():
    """Dashboard overview of current system update"""
    logdir = last_date()
    if logdir:
        return Watch().run()
    else:
        sys.exit("No log directory found")
