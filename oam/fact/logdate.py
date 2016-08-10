#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import click
from oam.facts import facts
from oam.daylog import last_day, DayLog

def fact(day=last_day()):
    """Return a string represent the day a report is being run for"""
    return { 'logdate': os.path.basename(day) }

@facts.command()
def logdate():
    """A list of runs made for the day"""
    print(fact()['logdate'])
    return 0
