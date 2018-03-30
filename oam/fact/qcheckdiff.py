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

def fact(day=last_day()):
    """Return the differences between specified and previous-to-it qcheck run"""
    prevqcheck_file = '{}/{}/qcheck.log'.format(oam.settings.oam.logs.directory, prev_day(day))
    daycheck_file = '{}/{}/qcheck.log'.format(oam.settings.oam.logs.directory, day)
    result = []
    if os.path.isfile(prevqcheck_file) and os.path.isfile(daycheck_file):
        cmd = 'diff -u {} {}'.format(prevqcheck_file, daycheck_file)
        try:
            result = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as ex:
            result = ex.output
    return { 'qcheck_diff': result.decode('utf-8').replace('\t', '   ').splitlines() }

@facts.command()
@click.option('--day', default=last_day(), help='day qcheck log to process')
def qcheckdiff(day):
    """Diff between current and previous qcheck run"""
    pprint.pprint(fact(day)['qcheck_diff'])
    return 0
