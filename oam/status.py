# -*- coding: utf-8 -*-

from __future__ import print_function

import click
from .cmd import cli
from oam.daylog import last_day
from oam.facts import get_facts
from oam.report import Report

class Status(object):

    def __init__(self, day):
        self.day = day

    def run(self):
        return Report(get_facts(self.day)).render()

@cli.command()
@click.option('--day', default=last_day(), help='day logs to process')
def status(day):
    """Generate an on the fly status report for the server"""
    print(Status(day).run())
    return 0

