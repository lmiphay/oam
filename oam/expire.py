#!/usr/bin/python

import os
import sys
import logging
import glob
import tarfile
import shutil
import click
from .cmd import cli

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
        for day in sorted(glob.glob(self.logdir + '/20*'))[:-self.keeplogs]:
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
        for daytarfile in sorted(glob.glob(self.olddir + '/20*'))[:-self.keeplogs]:
            self.logger.log(logging.DEBUG, 'expire old %s', daytarfile)
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

@cli.command()
@click.option('--logdir', default=os.getenv('OAM_LOGDIR', '/var/log/oam'), help='location of logs directory')
@click.option('--keeplogs', default=int(os.getenv('OAM_KEEPLOGS', 10)), help='number of iterations of logs to keep')
@click.option('--dryrun/--no-dryrun', default=False, help='whether files should actually be removed')
def expire(logdir, keeplogs, dryrun):
    """Expire the gentoo-oam logfiles"""
    OAMExpire(logdir, keeplogs, dryrun).run()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    sys.exit(OAMExpire(len(sys.argv)>1).run())
