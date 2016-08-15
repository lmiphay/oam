#!/usr/bin/python

from __future__ import print_function
import sys
import os
import re
import click
from .cmd import cli

IS_KEYWORD_USE_CHANGE = r'^>|^='
""" Failed record:
 *
 * The following package has failed to build, install, or execute postinst:
 *
 *  (sci-visualization/kst-2.0.8:0/0::gentoo, ebuild scheduled for merge), Log file:
 *   '/var/tmp/portage/portage/sci-visualization/kst-2.0.8/temp/build.log'
 *
"""
IS_FAILED_PACKAGE = r'^ \*  \(([-\w\./]+)'
    # trim down the noise a bit by filtering lines with any of this text
FILTER = (
    r'created log file|'
    'The following |'
    'postinst:|'
    'ebuild scheduled for merge|'
    'After world updates,|'
    'emerge --depclean.|'
    'Use --autounmask-write|'
    'Carefully examine the list|'
    'paying special attention|'
    'experimental or unstable packages|'
    'It may be possible|'
    'prevent one of those|'
    'possible that confl|'
    'impossible to satisfy|'
    'the dependencies of|'
    'not be installed simultaneously.|'
    'For more information, see|'
    'page or refer to the Gentoo Handbook.|'
    'Multiple package instances|'
    'into the dependency graph|'
    ' +\^|'
    '^# required by .+$|'
    'WARNING: One or more'
)

""" Process one or more block.log files and summarise any problems
"""
class Blocks(object):

    def __init__(self):
        self.filter_re = re.compile(FILTER) # not strictly necessary, but to be safe
        self.seen = set()                      # used to avoid repeating messages
        self.kw_use = []                       # keyword/use changes required
        self.failed = set()                    # packages which failed to build/install
        self.misc = []                         # other misc problem messages

    def report_category(self, msg, content, index=''):
        print(msg)
        for item in content:
            print(index, item)

    def report(self):
        """Dump processed results to stdout"""
        self.report_category('errors/blocked packages', self.misc, 'E ')
        self.report_category('packages which failed to install', self.failed, 'I ')
        self.report_category('required keyword/use changes', self.kw_use, 'K ')

    def handle_failed(self, line):
        """Look for failed package messages and record them"""
        result = re.search(IS_FAILED_PACKAGE, line)
        if result:
            self.failed.add(result.groups()[0])
            return True
        else:
            return False

    def handle_misc(self, line):
        """Record other failure messages"""
        line = re.sub(r'^ \* ', '', line).strip()
        if len(line)>0 and line not in self.seen:
            self.seen.add(line)
            self.misc.append(line.strip())

    def process_line(self, line):
        """Process one line looking for block info"""
        #print('process:{}<<'.format(line))
        if not self.filter_re.search(line): # drop noise lines early
            if re.search(IS_KEYWORD_USE_CHANGE, line):
                if line not in self.seen:
                    self.seen.add(line)
                    self.kw_use.append(line.strip())
            else:
                if not self.handle_failed(line):
                    self.handle_misc(line)
        #else:
        #    print('drop:', line.strip())

    def process_file(self, filename):
        """Process one file for blocked packages"""
        with open(filename, 'r') as rdr:
            #self.misc.append('Processing: {}'.format(filename))
            for line in rdr:
                self.process_line(line)

    def run(self, filenames):
        """Process one or more files for blocked packages"""
        for filename in filenames:
            if os.path.isfile(filename):
                self.process_file(filename)
        return self

@cli.command()
@click.argument('blockfiles', nargs=-1)
def blocksummary(blockfiles):
    """Summarise blocks/merge-failures"""
    Blocks().run(blockfiles).report()
    return 0
