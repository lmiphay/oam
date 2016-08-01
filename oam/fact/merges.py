#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
import logging
import glob
import click

from oam.facts import facts
from oam.daylog import last_day, DayLog
from oam.merges import Merges

def fact(day = last_day()):
    """Return a list of merges made for the day"""
    runfiles = DayLog(day).runfiles('merge.log')
    return { 'merges': list(Merges().run(runfiles).actual()) }

@facts.command()
def merges():
    """A list of merges made for the day"""
    print('\n'.join(fact()['merges']))
    return 0
