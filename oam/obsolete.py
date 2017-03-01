# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import logging
import click
import subprocess
import re
from .cmd import cli

"""
    Wrapper around: eix --test-non-matching --test-obsolete --exact
    check for obsolete portage configuration entries
"""
class Obsolete(object):

    CMD = ['eix', '--test-non-matching', '--test-obsolete', '--exact']
    FILTER = {'No non-matching',
              'No matches found',
              'The names of all installed packages are in the database',
              '--'
              }
    SECTION = [
        'Non-matching entries in /etc/portage/package.keywords',
        'The following installed packages are not in the database'
    ]

    def __init__(self):
        pass

    def its(self):
        """Return a list obsolete portage configuration entries, filtering noise"""
        rdr = subprocess.Popen(self.CMD, stdout=subprocess.PIPE)
        for line in rdr.stdout:
            if len(line)>1 and not any(line.startswith(s) for s in self.FILTER):
                yield line.strip()

# installed package list that currently requires keywording
# add: enalyze --no-color rebuild keywords --pretend --exact

# use flag settings that are currently required by installed packages
# add: enalyze --no-color rebuild use --pretend --exact
#    : maybe filter - abi_x86_32, -linguas_*, -sane_backends_*

@cli.command()
def obsolete():
    """check for obsolete portage configuration entries"""
    for it in Obsolete().its():
        print(it)
    return 0
