#!/usr/bin/python

from __future__ import print_function
import sys
import os
import logging
import click
import subprocess
import re
import datetime
import time
import glob
from .cmd import cli

class DayLog(object):

    def today(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')

    def __init__(self):
        self.log_dir = os.getenv('OAM_LOGDIR', '/var/log/oam')
        self.starting_day = self.today()

    def current_day(self):
        return self.starting_day

    def last_day(self):
        return sorted(glob.glob(self.log_dir + '/2*'))[-1]

DAYLOG = DayLog()

@cli.command()
@click.pass_context
def daylog(ctx):
    """Return the current day directory name"""
    print(DAYLOG.current_day())
    return 0

@cli.command()
@click.pass_context
def lastday(ctx):
    """
    Return the last day we appear to have log files for; eg.
    /var/log/oam/20160403
    """
    print(DAYLOG.last_day())
    return 0
