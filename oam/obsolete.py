# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import logging
import click
import subprocess
import re
from oam.cmd import cli

TESTING_PACKAGES = 'enalyze --no-color rebuild keywords --pretend --exact'
EIX = '/usr/bin/eix'
CMD = [EIX, '--test-non-matching', '--test-obsolete', '--exact']
FILTER = {'No non-matching',
          'No matches found',
          'The names of all installed packages are in the database',
          '--',
          'Total number of entries in report =',
          '  -- These are the installed packages & keywords that were detected',
          '     to need keyword settings other than the defaults.'
}
SECTIONS = {
    'Non-matching entries in /etc/portage/package.keywords:': 'keywords',
    'Non-matching entries in /etc/portage/package.mask:': 'mask',
    'Non-matching entries in /etc/portage/package.unmask': 'unmask',
    'Non-matching or empty entries in /etc/portage/package.use:': 'use',
    'The following installed packages are not in the database:': 'unknown'
}


class Obsolete(object):
    """
    Wrapper around: eix --test-non-matching --test-obsolete --exact
    check for obsolete portage configuration entries
    """

    def its(self):
        """Return a list obsolete portage configuration entries, filtering noise; needs
           eix
        """
        if os.path.isfile(EIX) and os.path.isfile('/var/cache/eix/portage.eix'):
            rdr = subprocess.Popen(CMD, stdout=subprocess.PIPE)
            for line in rdr.stdout:
                line = line.decode('utf-8')
                if len(line)>1 and not any(line.startswith(s) for s in FILTER):
                    yield line.strip()
        else:
            yield '(eix not installed)'

    def testing_packages():
        """installed package list that currently requires keywording"""
        for line in rdr.subprocess.Popen(TESTING_PACKAGES, shell=True, stdout=subprocess.PIPE).stdout:
            if len(line)>1 and not any(line.startswith(s) for s in FILTER):
                yield line.strip()

# use flag settings that are currently required by installed packages
# add: enalyze --no-color rebuild use --pretend --exact
#    : maybe filter - abi_x86_32, -linguas_*, -sane_backends_*

@cli.command()
def obsolete():
    """check for obsolete portage configuration entries"""
    for it in Obsolete().its():
        print(it)
    return 0
