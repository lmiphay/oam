#!/usr/bin/python

import sys
import os
import subprocess
import logging

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

    def filter(self, line):
        return line in self.SKIPLINES or lines.startswith('Calculating dependencies')
        
    def run(self):
        self.logger.log(logging.DEBUG, 'pretend cmd: %s', str(self.CMD))
        self.logger.log(logging.DEBUG, 'running pretend for: %s', self.target)
        try:
            for line in subprocess.check_output(self.CMD + [self.target],
                                                stderr=subprocess.STDOUT).splitlines():
                if not self.filter(line):
                    print(line)
        except subprocess.CalledProcessError as e:
            self.logger.log(logging.ERROR, 'pretend failed for: %s', self.target)
            self.logger.log(logging.ERROR, 'failure details: %s', str(e))

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
        
