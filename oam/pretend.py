#!/usr/bin/python

import sys
import os
import subprocess
import logging

class Pretend:
    
    CMD = ['emerge', '--update', '--backtrack=50', '--deep', '--pretend', '-v']

    def __init__(self, target = 'world'):
        self.target = target
        
    def run(self):
        try:
            print(subprocess.check_output(self.CMD + [self.target],
                                          stderr=subprocess.STDOUT))
        except subprocess.CalledProcessError as e:
            print('failed with: '+ str(e))

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
        
