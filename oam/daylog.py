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
from .cmd import cli

class DayLog(object):

    def today(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')

    def __init__(self):
        self.starting_day = self.today()

    def current_day(self):
        return self.starting_day

DAYLOG = DayLog()

@cli.command()
@click.pass_context
def daylog(ctx):
    """Return the current day directory name"""
    print(DAYLOG.current_day())
    return 0
