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
            self.logger.log(logging.DEBUG, 'checking %s', day)
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
            self.logger.log(logging.DEBUG, 'expire old %s', day)
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

    @staticmethod
    def usage():
        return "usage: " + os.path.basename(sys.argv[0]) + " [-h] <logdir> <keeplogs> <dryrun>"

    @staticmethod
    def create(argv):
        if len(argv) == 4:
            return OAMExpire(argv[1], int(argv[2]), argv[3] == 'True')
        elif len(argv) == 2:
            return OAMExpire()
        elif len(argv) == 2 and argv[1] == '-h':
            sys.exit(OAMExpire.usage())
        else:
            sys.exit(OAMExpire.usage())

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    sys.exit(OAMExpire.create(sys.argv).run())
