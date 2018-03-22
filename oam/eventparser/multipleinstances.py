# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import subprocess
import logging
import glob
import collections
import unittest
import re

from oam.eventparser.report import Report
from oam.eventparser.scanner import Scanner

class MultipleInstances:

    RECORD= r".+(Multiple package instances).+|"\
            ".+\(([-:/\w.]+), ebuild scheduled for merge\) pulled in.*|"\
            ".+\(([-:/\w.]+), installed\) pulled.*|"\
            ".+(It may be possible).+"
    TAG = 'MultipleInstances'

    def __init__(self):
        self.ev = None
        self.logger = logging.getLogger("oam.eventparser.multipleinstances")

    def emit(self):
        if self.ev:
            self.result = self.ev
            self.ev = None

    def process(self, line, match):
        self.result = None
        start, pkg_1, pkg_2, finish = match.groups()
        if pkg_1:
            self.emit()
            self.ev = [self.TAG, pkg_1]
        elif pkg_2:
            self.ev.append(pkg_2)
            self.emit()
        elif finish:
            self.emit()
        self.logger.log(logging.DEBUG, "got event: %s %s", str(self.result), str(match.groups()))
        return self.result

class MultipleInstancesTestCase(unittest.TestCase):

    MULTIPLEINSTANCES = """
!!! Multiple package instances within a single package slot have been pulled
!!! into the dependency graph, resulting in a slot conflict:

x11-drivers/nvidia-drivers:0

  (x11-drivers/nvidia-drivers-358.16-r1:0/358::gentoo, ebuild scheduled for merge) pulled in by
    (no parents that aren't satisfied by other packages in this slot)

  (x11-drivers/nvidia-drivers-355.11-r2:0/355::gentoo, installed) pulled in by
    x11-drivers/nvidia-drivers:0/355 required by (media-video/nvidia-settings-355.11:0/0::gentoo, ebuild scheduled for merge)
                              ^^^^^^


It may be possible to solve this problem by using package.mask to
prevent one of those packages from being selected. However, it is also
possible that conflicting dependencies exist such that they are
impossible to satisfy simultaneously.  If such a conflict exists in
the dependencies of two different packages, then those packages can
not be installed simultaneously.

For more information, see MASKED PACKAGES section in the emerge man
page or refer to the Gentoo Handbook.
"""

    def setUp(self):
        self.logger = logging.getLogger("oam.eventparser.multipleinstances.test")

    def test_multipleinstances(self):
        report = Report.from_string(self.MULTIPLEINSTANCES)
        scanner = Scanner(report, [MultipleInstances()])
        for ev in scanner.parse():
            report.add_event(ev)
            self.logger.log(logging.INFO, "event: %s", str(ev))
        self.assertEqual(report.count(), 1)
        report.report()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s')

    unittest.main()
