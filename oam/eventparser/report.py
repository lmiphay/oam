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

class Report:

    def __init__(self, lines):
        self.lines = lines
        self.event = []
        self.used = [list() for x in lines]
        self.logger = logging.getLogger("oam.eventparser.report")

    @classmethod
    def from_file(cls, name):
        return cls([line.strip() for line in open(name, 'r')])
    
    @classmethod
    def from_string(cls, s):
        return cls(s.splitlines())

    def scan(self):
        for line, i in zip(self.lines, xrange(len(self.lines))):
            yield (line, i)

    def consume(self, num, ident):
        self.logger.log(logging.DEBUG, "consume: %d, %s", num, ident)
        self.used[num].append(ident)

    def add_event(self, ev):
        self.event.append(ev)
        
    def count(self):
        return len(self.event)
    
    def report_unmatched(self):
        for use, line in zip(self.used, self.lines):
            if len(use)==0 and len(line)>0: # no parser claimed this line
                print('UNCLAIMED: ', line)
            elif len(use)>1: # more than one parser saw this line
                print('MULTIPLE-CLAIMS: ', str(use), line)
        
    def report(self):
        for ev in self.event:
            print("%s\t%s" % (ev[0], ', '.join(ev[1:])))
        self.report_unmatched()
        
class ReportTestCase(unittest.TestCase):

    def setUp(self):
        self.logger = logging.getLogger("oam.eventparser.report.test")

    def test_report(self):
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
