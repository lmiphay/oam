# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os
import subprocess
import logging
import datetime
import click
from .cmd import cli
import oam.settings

LOGFILE = oam.settings.oam.emerge.log

class EmergeLog(object):

    def __init__(self, logfile=LOGFILE):
        self.logfile = logfile
        self.ts_format = oam.settings.oam.ts

    def timestamp(self, raw_format):
        return datetime.datetime.fromtimestamp(int(raw_format)).strftime(self.ts_format)

    def last_line(self):
        return subprocess.check_output(['tail', '-1', self.logfile])

    def package_name(self, line, field_num):
        return line.split(' ')[field_num].strip('()') # -e 's/::.*//'

    def status(self, line):
        pass

    def run(self):
        self.proc = subprocess.Popen(['tail', '-F', self.logfile], stdout=subprocess.PIPE)
        while 1:
            line = self.proc.stdout.readline().decode('utf8').rstrip()
            field = line.split(':  ', 1)
            if len(field) == 2:
                print(self.timestamp(field[0]), field[1])
            else:
                print(line)

@cli.command()
def emergelog():
    """Tail /var/log/emerge.log with readable times"""
    EmergeLog().run()
