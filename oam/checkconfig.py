# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import stat
import grp
import pwd
import glob
import click
from .cmd import cli
import oam.settings

EXPIRE_LOG = '{}/expire.log'.format(oam.settings.oam.logs.directory)

class CheckConfig(object):
    """ Check:
        1. readability, ownership... etc of specified files and directories.
        2. try and detect if cron is running (presence of /var/log/oam/expire.log)
    """

    USER  = 'root' # expect to find files owned by this user
    GROUP = 'oam'  # expect to find this group ownership

    DEFAULT_TARGETS = [
        ('file', '/etc/oam/oam.yaml',     [ ('mode',0o640), ('group',GROUP), ('owner',USER) ] ),
        ('dir',  '/etc/oam/conf.d',       [ ('mode',0o750), ('group',GROUP), ('owner',USER) ] ),
        ('glob', '/etc/oam/conf.d/*',     [ ('mode',0o640), ('group',GROUP), ('owner',USER) ] ),
        ('dir',  '/var/log/oam',          [ ('mode',0o770), ('group',GROUP), ('owner',USER) ] ),
    ]

    # we can only check this one when running as root - the default is for the contents of /etc/cron.daily
    # to be readable by root or group-root users only.
    ROOT_TARGETS = DEFAULT_TARGETS + [
        ('file', '/etc/cron.daily/oam',                  [ ('mode',0o755), ('group','root'), ('owner',USER) ] ),
        ('file', '/etc/cron.monthly/oam-depclean-check', [ ('mode',0o755), ('group','root'), ('owner',USER) ] )
    ]

    def __init__(self):
        self.result = 0
        self.msg = None

    def report(self, message):
        if self.msg != None:
            self.msg.append(message)
        else:
            print(message)
            
    def fail(self, message):
        self.result += 1
        self.report(message)

    def mode(self, filename):
        return stat.S_IMODE(os.stat(filename).st_mode)

    def owner(self, filename):
        return pwd.getpwuid(os.stat(filename).st_uid)[0]

    def group(self, filename):
        return grp.getgrgid(os.stat(filename).st_gid)[0]

    def check_exist(self, spec):
        return os.path.exists(spec[0])

    def check_mode(self, pathspec, required):
        return self.mode(pathspec) == required

    def check_owner(self, pathspec, required):
        return self.owner(pathspec) == required

    def check_group(self, pathspec, required):
        return self.group(pathspec) == required

    CHECKS = {
        'mode':  (check_mode,  mode,  'chmod '),
        'group': (check_group, group, 'chown :'),
        'owner': (check_owner, owner, 'chown ')
    }

    def format(self, checktype, val):
        """ python 3: Octal literals are no longer of the form 0720; use 0o720 instead.
        """
        if sys.version_info > (3,0):
            return '0' + str(oct(val))[2:] if checktype=='mode' else str(val)
        else:
            return str(oct(val)) if checktype=='mode' else str(val)

    def check_target(self, pathspec, checks):
        for chk, val in checks:
            if chk in self.CHECKS:
                if not self.CHECKS.get(chk)[0](self, pathspec, val):
                    self.fail('# ' + pathspec + ' failed check for ' + chk + ' = ' +
                              self.format(chk, val) +
                              ', actual=' +
                              self.format(chk, self.CHECKS.get(chk)[1](self, pathspec)))
                    self.report(self.CHECKS.get(chk)[2] + self.format(chk, val) + ' ' + pathspec)
            else:
                self.fail(checktype + ' is not available')

    def check_file(self, pathspec, checks):
        if os.path.isfile(pathspec):
            self.check_target(pathspec, checks)
        else:
            self.fail('# ' + pathspec + ' is not a file (or is not accessible)')

    def check_dir(self, pathspec, checks):
        if os.path.isdir(pathspec[0]):
            self.check_target(pathspec, checks)
        else:
            self.fail(spec[0], 'is not a dir (or is not accessible)')

    def check_glob(self, pathspec, checks):
        for filename in glob.glob(pathspec):
            self.check_target(filename, checks)

    TYPES = {
        'file':check_file,
        'dir':check_dir,
        'glob':check_glob
    }

    def process(self, targets = DEFAULT_TARGETS):
        for checktype, pathspec, checks in targets:
            if checktype in self.TYPES:
                self.TYPES.get(checktype)(self, pathspec, checks)
            else:
                self.fail(checktype + ' is not available')

        return self.result

    def its(self):
        self.msg = []
        self.run()
        return self.msg

    def cron_has_run(self):
        return os.path.exists(EXPIRE_LOG)

    def run(self):
        if os.geteuid() == 0:
            result = self.process(CheckConfig.ROOT_TARGETS)
        else:
            self.report('# /etc/cron.daily/oam not checked')
            result = self.process(CheckConfig.DEFAULT_TARGETS)

        if not self.cron_has_run():
            result = False
            self.report('### cron has not run yet ###')

        if result == 0:
            self.report('### PASS ###')
        else:
            self.report('### FAIL ###')

        return result

@cli.command()
def checkconfig():
    """Check modes/owners of oam files/dirs"""
    CheckConfig().run()
