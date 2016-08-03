#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import subprocess
import logging
import click

from oam.facts import facts
from oam.daylog import last_day, DayLog

def fact(day = last_day()):
    """Return the differences between current and previous qcheck run"""
    prefdate = ''
    prevdir = '{}/qcheck.log'
    daydir = '{}/qcheck.log'
    if os.path.isfile(prevqcheck_file) and os.path.isfile(daycheck_file):
        cmd = 'diff -u {} {} '.format(prevqcheck_file, daycheck_file)
        return { 'qcheck_diff': subprocess.check_output(cmd, shell=True).splitlines() }
    else:
        return { 'qcheck_diff': '' }

@facts.command()
def qcheckdiff():
    """Differences between current and previous qcheck run"""
    print(fact()['qcheck_diff'])
    return 0

#PREVDATE=$(oam_prevdate $LOGDATE)
#if [[ -f $LOGDATE/qcheck.log && -f $PREVDATE/qcheck.log ]] ; then
#    diff -u $PREVDATE/qcheck.log $LOGDATE/qcheck.log 
#fi

#oam_prevdate()
#{
#    local laterdate=$1
#
#    (cd $OAM_LOGDIR && ls -d1 20* |grep --before-context=1 $laterdate | head -1)
#}
