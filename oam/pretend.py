#!/usr/bin/python

import sys
import os
import subprocess
import logging
import re

""" A wrapper around emerge --update --pretend world, which filters some noise out and
    in addition produces an ordered list of the packages which would be merged in a format
    suitable for feeding back into emerge.
"""
class Pretend:
    
    CMD = ['emerge', '--update', '--backtrack=50', '--deep', '--pretend', '-v']

    SKIPLINES = {
        'These are the packages that would be merged, in order:',
        'Total: 0 packages, Size of downloads: 0 KiB',
        ' * Use eselect news read to view new items.',
        ''
        }

    def __init__(self, target = 'world'):
        self.target = target
        self.logger = logging.getLogger("oam.pretend")
        self.packages = set()

    def filter(self, line):
        return line in self.SKIPLINES or line.startswith('Calculating dependencies')

    def add_package_name(self, line):
        """ parse emerge output for package specifiers; e.g.
              [ebuild     U ~] media-video/nvidia-settings-355.11::gentoo....
            ignore these type of records:
              [uninstall     ] dev-python/dnspython-1.11.1::gentoo....
              [blocks b      ] dev-python/dnspython:0....
        """
        if line.startswith('[ebuild'):
            self.packages.add(re.sub(r'^\[[^]]+\] ([^:]+).+', r'=\1', line))

    def dump_packages(self):
        if len(self.packages) > 0:
            print('Sorted merge list:')
            for pkg in self.packages:
                print(pkg)

    def run(self):
        self.logger.log(logging.DEBUG, 'pretend cmd: %s', str(self.CMD))
        self.logger.log(logging.DEBUG, 'running pretend for: %s', self.target)
        try:
            for line in subprocess.check_output(self.CMD + [self.target],
                                                stderr=subprocess.STDOUT).splitlines():
                if not self.filter(line):
                    print(line)
                    self.add_package_name(line)
        except subprocess.CalledProcessError as e:
            self.logger.log(logging.ERROR, 'pretend failed for: %s', self.target)
            self.logger.log(logging.ERROR, 'failure details: %s', str(e))
        self.dump_packages()

    @staticmethod
    def usage():
        return "usage: " + os.path.basename(sys.argv[0]) + " pretend [-h] [<target>]"

    @staticmethod
    def create(argv):
        if len(argv) == 2 and argv[1] == '-h':
            sys.exit(Pretend.usage())
        elif len(argv) == 2:
            return Pretend(argv[1])
        elif len(argv) == 1:
            return Pretend()
        else:
            sys.exit(Pretend.usage())

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    sys.exit(Pretend.create(sys.argv).run())
        
