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
import re
from .cmd import cli

def today():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')

class DayLog(object):

    def __init__(self, day=today()):
        self.log_dir = os.getenv('OAM_LOGDIR', '/var/log/oam')
        self.starting_day = day

    def log_dir(self):
        return log_dir

    def current_day(self):
        return self.starting_day

    def last_day(self):
        datedir = self.timed_runs()
        if len(datedir) > 0:
            return datedir[-1]
        else:
            return None

    def day_runs(self):
        return sorted(filter(re.compile(r'\d{8}').match, os.listdir(self.log_dir)))

    def timed_runs(self):
        return sorted(filter(re.compile(r'\d{6}').match, os.listdir("{}/{}".format(self.log_dir, self.current_day()))))

DAYLOG = DayLog()

@cli.command()
def logdir():
    """Return the configured oam log directory"""
    print(DAYLOG.log_dir())
    return 0

@cli.command()
def daylog():
    """Return the current day directory name"""
    print(DAYLOG.current_day())
    return 0

@cli.command()
def lastday():
    """
    Return the last day we appear to have log files for; eg.
    /var/log/oam/20160403
    """
    print(DAYLOG.last_day())
    return 0

@cli.command()
def dayruns():
    """Return the list of runs"""
    print(DAYLOG.day_runs())
    return 0

@cli.command()
def timedruns():
    """Return the list of runs for the current day"""
    print(DAYLOG.timed_runs())
    return 0
