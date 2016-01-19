#!/usr/bin/python

import sys
import os
import subprocess
import logging
import glob
import collections

class Pkg:

    ROOT = os.getenv('PORTAGE_CONFIGROOT', '') + '/var/db/pkg/'

    def __init__(self):
        pass

    def package(self, path):
        return os.path.relpath(path, self.ROOT)
                          
    def sizes(self):
        rec = collections.defaultdict(list)
        for filename in glob.iglob(self.ROOT + '*/*/SIZE'):
            size = int(open(filename).readline().strip())
            rec[size].append(self.package(os.path.dirname(filename)))
        for size, pkgs in sorted(rec.iteritems()):
            for p in pkgs:
                print("%10d %s" % (size, p))
    
    def current_pkgs(self):
        pass

    def delta(self):
        pass

    def changed(self, package):
        pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    sys.exit(Pkg().sizes())
