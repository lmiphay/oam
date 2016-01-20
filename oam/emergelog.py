#!/usr/bin/python

import sys
import os
import subprocess
import logging
from datetime import datetime

class EmergeLog:

    LOGFILE = '/var/log/emerge.log'

    def __init__(self):
        self.proc = subprocess.Popen(['tail', '-F', self.LOGFILE], stdout=subprocess.PIPE)
        self.ts_format = os.getenv('OAM_TS', '%Y%m%d:%H:%M:%S')

    def run(self):
        while 1:
            line = self.proc.stdout.readline()
            field = line.split(':', 1)
            if len(field) == 2:
                print datetime.fromtimestamp(int(field[0])).strftime(self.ts_format), field[1],

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    sys.exit(EmergeLog().run())
