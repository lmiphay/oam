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

LOG_DIR = os.getenv('OAM_LOGDIR', '/var/log/oam')

def today():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')

def day_runs():
    return sorted(filter(re.compile(r'\d{8}').match, os.listdir(LOG_DIR)))

def last_day():
    datedir = day_runs()
    if len(datedir) > 0:
        return datedir[-1]
    else:
        return None

class DayLog(object):

    def __init__(self, day=today()):
        self.day = day
        self.day_dir = "{}/{}".format(LOG_DIR, day)

    def day_dir(self):
        return self.day_dir

    def current_day(self):
        return self.day

    def timed_runs(self):
        if os.path.isdir(self.day_dir):
            return sorted(filter(re.compile(r'\d{6}').match, os.listdir(self.day_dir)))
        else:
            return []

DAYLOG = DayLog()

@cli.command()
def logdir():
    """Return the configured oam log directory"""
    print(LOG_DIR)
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
    print(last_day())
    return 0

@cli.command()
def dayruns():
    """Return the list of runs"""
    print(day_runs())
    return 0

@cli.command()
def timedruns():
    """Return the list of runs for the current day"""
    print(DAYLOG.timed_runs())
    return 0

@cli.command()
def lasttimedruns():
    """Return the list of runs for the last day"""
    print(DayLog(last_day()).timed_runs())
    return 0
