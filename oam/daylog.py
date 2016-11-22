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

def timestamp():
    return time.strftime('%Y%m%d:%H:%M:%S')

def today():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')

def day_runs():
    return sorted(filter(re.compile(r'\d{8}').match, os.listdir(LOG_DIR)))

def last_day():
    """Return the most recent day we have an oam run for; e.g. 20160801"""
    datedir = day_runs()
    if len(datedir) > 0:
        return datedir[-1]
    else:
        return None

def prev_day(start_day):
    """Return the previous day to start dat for which we have an oam run for; e.g. 20160801"""
    datedir = day_runs()
    if start_day in datedir:
        prev_index = datedir.index(start_day) - 1
        if prev_index >= 0:
            return datedir[prev_index]
    return None

def get_logfile(ident):
    """ Return a fully qualified filename of the form /var/log/oam/<TODAY>/<ident.log>
        Directory and file created as required.
    """
    dirname = '{}/{}'.format(LOG_DIR, today())
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    filename = '{}/{}.log'.format(dirname, ident)

    if not os.path.isfile(filename):
        with open(filename, 'w') as wtr:
            wtr.write('{} created log file\n'.format(timestamp()))

    return filename

class DayLog(object):

    def __init__(self, day=today()):
        self.day = day
        self.daydir = "{}/{}".format(LOG_DIR, day)

    def day_dir(self):
        return self.daydir

    def current_day(self):
        return self.day

    def timed_runs(self):
        if os.path.isdir(self.daydir):
            return sorted(filter(re.compile(r'\d{6}').match, os.listdir(self.daydir)))
        else:
            return []

    def runfiles(self, name):
        return sorted(glob.glob('{}/*/{}'.format(self.daydir, name)))

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

@cli.command()
@click.argument('ident') # help='create a log file <ident>.log'
def logfile(ident):
    """Return the list of runs for the last day"""
    print(get_logfile(ident))
    return 0
