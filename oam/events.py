#!/usr/bin/python

from __future__ import print_function
import sys
import os
import subprocess
import logging
import glob
import collections
import click
from .cmd import cli

from .eventparser.report import Report
from .eventparser.scanner import Scanner

class Events:

    def __init__(self, datedir):
        self.logger = logging.getLogger("oam.events")
        self.datedir = datedir
        self.report = Report.from_file(datedir)
        self.scanner = Scanner(self.report, [BuildFail()])

    def run(self):
        for ev in self.scanner.parse():
            self.report.add_event(ev)
            self.logger.log(logging.DEBUG, "event: %s", str(ev))
        self.report.report()

@cli.command()
@click.argument('datedir')
def events(datedir):
    """Report errors encountered during merges"""
    Events(datedir).run()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    sys.exit(Events(sys.argv[1]).run())
