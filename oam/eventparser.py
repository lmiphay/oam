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

class BuildFailEventParser():

    RECORD= r".+\(([-:/\w\.]+), ebuild scheduled for merge.+|.+'([-/\w\.]+)/temp/build.log.*"
    
    def __init__(self):
        self.logger = logging.getLogger("oam.event.parser.buildfail")

    def parse(self, lines):
        ev = None
        for line in lines:
            self.logger.log(logging.DEBUG, "line: %s", line)
            match = re.search(self.RECORD, line)
            if match:
                pkg_name, build_log = match.groups()
                if pkg_name:
                    if ev: yield ev
                    ev = ['Build Fail', pkg_name]
                elif build_log:
                    ev.append(build_log + '/temp/build.log')
                    yield ev
                    ev = None
        if ev: yield ev

class KeywordChangeEventParser():

    RECORD = r'^# required by (.+)|^=(.+)'
    
    def __init__(self):
        self.logger = logging.getLogger("oam.event.parser.keywordchange")

    def parse(self, lines):
        ev = ['Keyword Change']
        for line in lines:
            self.logger.log(logging.DEBUG, "line: %s", line)
            match = re.search(self.RECORD, line)
            if match:
                required_by, keyword = match.groups()
                if required_by:
                    ev.insert(1, required_by)
                elif keyword:
                    ev.insert(1, '=' + keyword)
                    yield ev
                    ev = ['Keyword Change']
        if len(ev)>1: yield ev
        
class EventParser:

    def __init__(self, logfile):
        self.logfile = logfile
        self.logger = logging.getLogger("oam.event.parser")
        self.parser = [KeywordChangeEventParser(), BuildFailEventParser()]
        self.event = []

    def run(self):
        data = [line.strip() for line in open(self.logfile, 'r')]
        for parser in self.parser:
            for ev in parser.parse(data):
                print("%s\t%s" % (ev[0], ', '.join(ev[1:])))
                self.event.append(ev)
    @staticmethod
    def usage():
        return "usage: " + os.path.basename(sys.argv[0]) + "  <logfile>"

    @staticmethod
    def create(argv):
        if len(argv) == 2 and argv[1] == '-h':
            sys.exit(EventParser.usage())
        elif len(argv) == 2:
            return EventParser(argv[1])
        else:
            sys.exit(EventParser.usage())

class EventParserTestCase(unittest.TestCase):

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
    
    KEYWORD_CHANGE="""
# required by kde-apps/kdebase-data-4.14.3-r1::gentoo[wallpapers]
# required by kde-apps/kdebase-runtime-meta-4.14.3::gentoo
# required by @selected
# required by @world (argument)
=kde-apps/kde-wallpapers-15.08.3 ~amd64
"""
    def setUp(self):
        self.logger = logging.getLogger("oam.event.parser.test")
        #self.parser = EventParser()

    def test_build_fail_single(self):
        p = BuildFailEventParser()
        events = []
        for ev in p.parse(self.BUILD_FAIL_1.splitlines()):
            events.append(ev)
            self.logger.log(logging.DEBUG, "event: %s", str(ev))
        self.assertEqual(len(events), 1)
        
    def test_build_fail_two(self):
        p = BuildFailEventParser()
        events = []
        for ev in p.parse(self.BUILD_FAIL_2.splitlines()):
            events.append(ev)
            self.logger.log(logging.DEBUG, "event: %s", str(ev))
        self.assertEqual(len(events), 2)
        
    def test_keyword_change(self):
        p = KeywordChangeEventParser()
        events = []
        for ev in p.parse(self.KEYWORD_CHANGE.splitlines()):
            events.append(ev)
            self.logger.log(logging.DEBUG, "event: %s", str(ev))
        self.assertEqual(len(events), 1)

if __name__ == '__main__':
    if len(sys.argv)==1:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
    
        unittest.main()
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
        
        sys.exit(EventParser(sys.argv[1]).run())
