# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import logging
import click
import subprocess
import re
from oam.cmd import cli

"""
    Wrapper around: qcheck --nomtime --nocolor
    check for bitrot/changes to installed packages
    looking for these type of lines only:
 AFK: /usr/share/icons/hicolor/192x192/apps
 MD5-DIGEST: /usr/lib64/gtk-3.0/3.0.0/immodules.cache
"""
class QCheck(object):

    CMD = ['qcheck', '--nomtime', '--nocolor']
    FILTER = {' AKF: ', ' MD5-DIGEST: '}

    def __init__(self):
        pass

    def is_interesting(self, line):
        return len(line)>1 and any(line.startswith(s) for s in self.FILTER)

    def its(self):
        """Return a list potential problems with installed packages"""
        for line in sorted(subprocess.Popen(self.CMD, stdout=subprocess.PIPE).stdout.readlines()):
            line = line.decode('utf-8')
            if self.is_interesting(line):
                yield line.strip()
          
@cli.command()
def qcheck():
    """check integrity of installed packages"""
    for it in QCheck().its():
        print(it)
    return 0
