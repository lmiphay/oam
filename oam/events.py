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

from .eventparser.buildfail import BuildFail
from .eventparser.multipleinstances import MultipleInstances
from .eventparser.skippedconflict import SkippedConflict

from .eventparser.report import Report
from .eventparser.scanner import Scanner

class Events:

    def __init__(self, blocks_logfile):
        self.logger = logging.getLogger("oam.events")
        self.blocks_logfile = blocks_logfile
        self.report = Report.from_file(blocks_logfile)
        self.scanner = Scanner(self.report, [BuildFail(), MultipleInstances(), SkippedConflict()])
        #self.scanner = Scanner(self.report, [MultipleInstances()])

    def run(self):
        for ev in self.scanner.parse():
            self.report.add_event(ev)
            self.logger.log(logging.INFO, "event: %s", str(ev))
        self.report.report()

@cli.command()
@click.argument('blocks_logfile')
def events(blocks_logfile):
    """Report errors encountered during merges"""
    Events(blocks_logfile).run()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    sys.exit(Events(sys.argv[1]).run())
