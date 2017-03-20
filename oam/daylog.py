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

def get_logfile(ident, mergelog=False):
    """ Return a fully qualified filename of the form:
        1. /var/log/oam/<TODAY>/<ident.log> (if mergelog is False)
        2. /var/log/oam/<TODAY>/<HOUR_MINUTES>/<ident.log> (if mergelog is True)
        Directory and file created as required. 
        If mergelog is True, then a symbolic link is created pointing to the file
        from /var/log/oam/<TODAY>/<ident.log>
    """
    daydir = '{}/{}'.format(LOG_DIR, today())
    if mergelog:
        subdir = time.strftime('%H%M%S')
        dirname = '{}/{}/{}'.format(LOG_DIR, subdir, today())
    else:
        dirname = daydir
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

    filename = '{}/{}.log'.format(dirname, ident)

    if not os.path.isfile(filename):
        with open(filename, 'w') as wtr:
            wtr.write('{} created log file\n'.format(timestamp()))

    if mergelog:
        symlink = '{}/{}.log'.format(daydir, ident)
        if os.path.islink(symlink):
            os.remove(symlink)
        os.symlink(os.path.relpath(filename, daydir), symlink)

    return filename

def get_logstream(ident, mergelog=False):
    return open(get_logfile(ident, mergelog), 'a')

def get_errstream():
    return open(get_logfile('error', mergelog=False), 'a')

def get_oamlogfile():
    return open(get_logfile('oam', mergelog=False), 'a')

def oamlog_write(msg):
    with get_oamlogfile() as f:
        f.write('{} {}\n'.format(timestamp(), msg))

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
