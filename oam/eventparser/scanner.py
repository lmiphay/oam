#!/usr/bin/python

from __future__ import print_function
import sys
import os
import subprocess
import logging
import glob
import collections
import unittest
import re

class Scanner:

    def __init__(self, report, checker):
        self.report = report
        self.checker = checker
        self.logger = logging.getLogger("oam.eventparser.scanner")

    def parse(self):
        for chk in self.checker:
            self.in_block = False
            for line, i in self.report.scan():
                match = re.search(chk.RECORD, line)
                self.logger.log(logging.INFO, "line: %d, %s", i, line)
                if match:
                    self.logger.log(logging.INFO, "parse-match: %s", str(match.groups()))
                    self.groups = match.groups()
                    if self.groups[0]:
                        self.in_block = True
                    elif self.groups[-1]:
                        self.in_block = False
                    elif self.in_block:
                        ev = chk.process(line, match)
                        if ev: yield ev
                if self.in_block:
                    self.report.consume(i, chk.TAG)
            if chk.ev != None: yield chk.ev

class ScannerTestCase(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("oam.eventparser.scanner.test")

    def test_scanner(self):
        pass
        
if __name__ == '__main__':
    if len(sys.argv)==1:
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)s %(message)s')
    
        unittest.main()
    else:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s')
        
        sys.exit(EventParser(sys.argv[1]).run())
