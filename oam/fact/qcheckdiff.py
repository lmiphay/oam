# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import subprocess
import logging
import pprint
import click

from oam.facts import facts
from oam.daylog import last_day, prev_day, DayLog
import oam.settings

def content(filename):
    try:
        return open(filename, 'r').read().replace('\t', '   ').splitlines()
    except Exception as ex:
        print(ex)
        return []

def fact(day=last_day()):
    """Return the differences between specified and previous-to-it qcheck run"""
    prevqcheck_file = '{}/{}/qcheck.log'.format(oam.settings.oam.logs.directory, prev_day(day))
    daycheck_file = '{}/{}/qcheck.log'.format(oam.settings.oam.logs.directory, day)
    if os.path.isfile(prevqcheck_file) and os.path.isfile(daycheck_file):
        result = ""
        cmd = 'diff -u {} {}'.format(prevqcheck_file, daycheck_file)
        try:
            result = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as ex:
            result = ex.output
        return { 'qcheck_diff': result.decode('utf-8').replace('\t', '   ').splitlines(),
                 'qcheck': content(daycheck_file)
        }
    else:
        if os.path.isfile(daycheck_file):
            return { 'qcheck_diff': "",
                     'qcheck': content(daycheck_file)
            }
        else:
            return { 'qcheck_diff': '',
                     'qcheck': ''
            }

@facts.command()
@click.option('--day', default=last_day(), help='day qcheck log to process')
def qcheckdiff(day):
    """Diff between current and previous qcheck run"""
    pprint.pprint(fact(day)['qcheck_diff'])
    return 0

@facts.command()
@click.option('--day', default=last_day(), help='day qcheck log to process')
def qcheck(day):
    """Current qcheck results"""
    pprint.pprint(fact(day)['qcheck'])
    return 0
