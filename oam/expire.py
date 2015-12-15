#!/usr/bin/python

import os
import sys
import logging
import glob
import tarfile
import shutil

class OAMExpire:

    def __init__(self, logdir = '/var/log/oam', keeplogs = 10, dryrun = False):
        self.logdir = logdir
        self.keeplogs = keeplogs
        self.dryrun = dryrun
        self.olddir = logdir + '/old'
        self.logger = logging.getLogger("oam.expire")

    def tarfilename(self, day):
        return self.olddir + '/' + os.path.basename(day) + '.tar.bz2'
    
    def backup(self, day):
        with tarfile.open(self.tarfilename(day), "w:bz2") as tar:
            tar.add(day)
            
    def process_daydirs(self):
        for day in glob.glob(self.logdir + '/20*')[:-self.keeplogs]:
            if os.path.isdir(day):
                if self.dryrun:
                    self.logger.log(logging.INFO, 'dryrun - backup, then remove %s', day)
                else:
                    self.logger.log(logging.INFO, 'backup/remove %s', day)
                    self.backup(day)
                    shutil.rmtree(day)
            else:
                self.logger.log(logging.ERROR, '%s is not a directory', day)
                break
         self.logger.log(logging.INFO, 'complete')

    def expire_old(self):
        for daytarfile in glob.glob(self.olddir + '/20*')[:-self.keeplogs]:
            if os.path.isfile(daytarfile):
                if self.dryrun:
                    self.logger.log(logging.INFO, 'dryrun - would remove %s', daytarfile)
                else:
                    self.logger.log(logging.INFO, 'removing %s', daytarfile)
                    os.remove(daytarfile)
                    
    def run(self):
        self.logger.log(logging.INFO, 'start; keeplogs=%d, dryrun=%s', self.keeplogs, self.dryrun)
        if os.path.isdir(self.logdir):
            self.process_daydirs()
        else:
            self.logger.log(logging.ERROR, '%s is missing', self.logdir)
        if os.path.isdir(self.olddir):
            self.expire_old()
        else:
            self.logger.log(logging.ERROR, '%s is missing', self.olddir)

def usage():
    return "usage: " + os.path.basename(sys.argv[0]) + " [-h] <logdir> <keeplogs> <dryrun>"
            
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    if len(sys.argv) == 4:
        sys.exit(OAMExpire.run(sys.argv[1], sys.argv[2], bool(sys.argv[3])))
    elif len(sys.argv) == 2 and sys.argv[1] == '-h':
        sys.exit(usage())
    else:
        sys.exit(usage())
