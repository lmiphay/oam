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
from report import Report
from scanner import Scanner

class SkippedConflict:

    RECORD = r".*(WARNING: One or more updates).+|"\
             "^([-:a-zA-Z0-9/\.]+)$|"\
             ".+\(([-:a-zA-Z0-9/.]+), ebuild scheduled for merge\) conflicts with.*|"\
             ".+ ([-:a-zA-Z0-9/\.]+ required by \([-:a-zA-Z0-9/\.]+), ebuild scheduled for merge.+|"\
             "^ (\*) .*"
    TAG = 'SkippedConflict'

    def __init__(self):
        self.ev = None
        self.logger = logging.getLogger("oam.eventparser.skippedconflict")
        
    def emit(self):
        if self.ev:
            self.result = self.ev
            self.ev = None
        
    def process(self, line, match):
        self.logger.log(logging.DEBUG, "process-match: %s", str(match.groups()))
        self.result = None
        start, pkg_name, scheduled, conflicts, finish = match.groups()
        if pkg_name:
            self.emit()
            self.ev = [self.TAG, pkg_name]
        elif scheduled:
            self.ev.append(scheduled)
        elif conflicts:
            self.ev.append(conflicts)
            self.emit()
        elif finish:
            self.emit()
        return self.result

class SkippedConflictTest(unittest.TestCase):

    SKIPPED_CONFLICT = """
WARNING: One or more updates/rebuilds have been skipped due to a dependency conflict:

x11-drivers/nvidia-drivers:0

  (x11-drivers/nvidia-drivers-358.16-r1:0/358::gentoo, ebuild scheduled for merge) conflicts with
    x11-drivers/nvidia-drivers:0/355 required by (media-video/nvidia-settings-355.11:0/0::gentoo, ebuild scheduled for merge)
                              ^^^^^^

 * 
"""
    def setUp(self):
        self.logger = logging.getLogger("oam.eventparser.skippedconflict.test")

    def test_skipped_conflict(self):
        report = Report.from_string(self.SKIPPED_CONFLICT)
        scanner = Scanner(report, [SkippedConflict()])
        for ev in scanner.parse():
            report.add_event(ev)
            self.logger.log(logging.DEBUG, "event: %s", str(ev))
        report.report()
        self.assertEqual(report.count(), 1)
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    unittest.main()
