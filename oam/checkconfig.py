#!/usr/bin/python
import sys
import os
import stat
import grp
import pwd
import glob

class CheckConfig:
    """ Check readability, ownership... etc of specified files and directories.
    """

    USER  = 'root' # expect to find files owned by this user
    GROUP = 'oam'  # expect to find this group ownership

    DEFAULT_TARGETS = [
        ('file', '/etc/gentoo-oam.conf',  [ ('mode',0o640), ('group',GROUP), ('owner',USER) ] ),
        ('dir',  '/etc/gentoo-oam.d',     [ ('mode',0o750), ('group',GROUP), ('owner',USER) ] ),
        ('glob', '/etc/gentoo-oam.d/*',   [ ('mode',0o640), ('group',GROUP), ('owner',USER) ] ),
        ('dir',  '/var/log/oam',          [ ('mode',0o770), ('group',GROUP), ('owner',USER) ] ),
    ]

    # we can only check this one when running as root - the default is for the contents of /etc/cron.daily
    # to be readable by root or group-root users only.
    ROOT_TARGETS = DEFAULT_TARGETS + [
        ('file', '/etc/cron.daily/gentoo-oam', [ ('mode',0o755), ('group','root'), ('owner',USER) ] )
    ]

    def __init__(self):
        self.result = 0

    def fail(self, message):
        self.result += 1
        print(message)

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
                    print(self.CHECKS.get(chk)[2] + self.format(chk, val) + ' ' + pathspec)
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

    def run(self):
        if os.geteuid() == 0:
            result = self.process(CheckConfig.ROOT_TARGETS)
        else:
            print('# /etc/cron.daily/gentoo-oam not checked')
            result = self.process(CheckConfig.DEFAULT_TARGETS)

        if result == 0:
            print('### PASS ###')
        else:
            print('### FAIL ###')

        return result

    @staticmethod
    def create(argv):
        return CheckConfig()

if __name__ == "__main__":

    sys.exit(CheckConfig().run())