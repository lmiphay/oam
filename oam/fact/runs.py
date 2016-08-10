#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
import logging
import click
from oam.facts import facts
from oam.daylog import last_day, DayLog

def fact(day=last_day()):
    """Return a list of runs made for the day"""
    return { 'runs': DayLog(day).timed_runs() }

@facts.command()
def runs():
    """A list of runs made for the day"""
    print(' '.join(fact()['runs']))
    return 0
