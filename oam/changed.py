#!/usr/bin/python

import sys
import os
import subprocess
import logging
import glob
import collections
import re
import yaml

""" support to track and manage lists of installed software
    oam changed dev-lang/python
    oam changed -u dev-lang/perl
"""
class Changed:

    ROOT = os.getenv('PORTAGE_CONFIGROOT', '') + '/var/db/pkg/'
    OAM_DB= '/var/db/oam/'

    def __init__(self, pkg_name, update = False):
        self.pkg_name = pkg_name
        self.update = update
        self.dirname = self.OAM_DB + pkg_name
        self.filename = self.dirname + '/versions'
        self.logger = logging.getLogger("oam.changed")
        self.logger.log(logging.DEBUG, 'changed for %s', self.pkg_name)
        self.logger.log(logging.DEBUG, 'last recorded installs(s)  %s', str(self.load()))
        self.logger.log(logging.DEBUG, 'portage current install(s) %s', str(self.current_versions()))
        self.logger.log(logging.DEBUG, 'has changed %s', str(self.changed()))

    def strip_rev(self, pkg):
        """ remove any trailing -r1... etc revision markers
        """
        return re.sub(r'(.+)-r\d+', r'\1', pkg)

    def current_versions(self):
        """ return a list which holds the currently installed version(s)
            of the specified package; (strip revision?) e.g.
            ['dev-lang/perl-5.20.2']
            ['dev-lang/python-2.7.10-r1', 'python-3.4.3-r1']
            note: exclude: dev-lang/python-exec-2.0.1-r1
        """
        return set([self.strip_rev(p) for p in glob.iglob(self.ROOT + self.pkg_name + '-[0-9]*')])

    def load(self):
        if os.path.exists(self.filename):
            return yaml.load(open(self.filename, 'r'))
        else:
            return set()

    def save(self):
        if not os.path.isdir(self.dirname):
            os.makedirs(self.dirname)
        yaml.dump(self.current_versions(), open(self.filename, 'w'))

    def changed(self):
        return self.current_versions() != self.load()

    def run(self):
        if self.update:
            self.save()
            return 0
        else:
            if self.changed():
                return 0
            else:
                return 1
        
    @staticmethod
    def usage():
        return "usage: " + os.path.basename(sys.argv[0]) + "  [-u] <package>"

    @staticmethod
    def create(argv):
        if len(argv) == 2 and argv[1] == '-h':
            sys.exit(Changed.usage())
        elif len(argv) == 2:
            return Changed(argv[1])
        if len(argv) == 3 and argv[1] == '-u':
            return Changed(argv[2], update=True)
        else:
            sys.exit(Changed.usage())

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    sys.exit(Changed.create(sys.argv).run())
