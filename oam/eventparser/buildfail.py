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

class BuildFail:

    RECORD= r".+(The following).+|"\
            ".+\(([-:/\w\.]+), ebuild scheduled for merge.+|"\
            ".+'([-/\w\.]+)/temp/build.log.*|"\
            ".+(After world).+"
    TAG = 'BuildFail'
    
    def __init__(self):
        self.ev = None
        self.logger = logging.getLogger("oam.eventparser.buildfail")
        
    def emit(self):
        if self.ev:
            self.result = self.ev
            self.ev = None
        
    def process(self, line, match):
        self.result = None
        start, pkg_name, build_log, finish = match.groups()
        if pkg_name:
            self.emit()
            self.ev = [self.TAG, pkg_name]
        elif build_log:
            self.ev.append(build_log + '/temp/build.log')
            self.emit()
        elif finish:
            self.emit()
        return self.result

class BuildFailTestCase(unittest.TestCase):

    BUILD_FAIL_1 ="""
 * The following package has failed to build, install, or execute postinst:
 * 
 *  (media-video/nvidia-settings-355.11:0/0::gentoo, ebuild scheduled for merge), Log file:
 *   '/var/tmp/portage/media-video/nvidia-settings-355.11/temp/build.log'
 * 
 * After world updates, it is important to remove obsolete packages with
 * emerge --depclean. Refer to `man emerge` for more information.
 * 
"""
    BUILD_FAIL_2 ="""
 * The following 2 packages have failed to build, install, or execute
 * postinst:
 * 
 *  (x11-base/xorg-server-1.17.4:0/1.17.4::gentoo, ebuild scheduled for merge), Log file:
 *   '/var/tmp/portage/x11-base/xorg-server-1.17.4/temp/build.log'
 *  (media-video/nvidia-settings-355.11:0/0::gentoo, ebuild scheduled for merge), Log file:
 *   '/var/tmp/portage/media-video/nvidia-settings-355.11/temp/build.log'
 * 
 * After world updates, it is important to remove obsolete packages with
 * emerge --depclean. Refer to `man emerge` for more information.
"""
    
    def setUp(self):
        self.logger = logging.getLogger("oam.eventparser.buildfail.test")

    def test_build_fail_single(self):
        report = Report.from_string(self.BUILD_FAIL_1)
        scanner = Scanner(report, [BuildFail()])
        for ev in scanner.parse():
            report.add_event(ev)
            self.logger.log(logging.DEBUG, "event: %s", str(ev))
        self.assertEqual(report.count(), 1)
        report.report()
        
    def test_build_fail_two(self):
        report = Report.from_string(self.BUILD_FAIL_2)
        scanner = Scanner(report, [BuildFail()])
        for ev in scanner.parse():
            report.add_event(ev)
            self.logger.log(logging.DEBUG, "event: %s", str(ev))
        self.assertEqual(report.count(), 2)
        report.report()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s')
    
    unittest.main()
