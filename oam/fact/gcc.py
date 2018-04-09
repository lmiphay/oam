# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
import logging
import pprint
import click
from oam.facts import facts

CURRENT_COMMAND = 'gcc-config --get-current-profile --nocolor'
LIST_COMMAND = 'gcc-config --list-profiles --nocolor'

def fact(day=None):
    """Return gcc compiler profile information"""
    current = subprocess.check_output(CURRENT_COMMAND, shell=True).decode('utf-8').splitlines()[0].strip()
    all_profiles = subprocess.check_output(LIST_COMMAND, shell=True).decode('utf-8').splitlines()

    return {
        'gcc': {
            'current': current,
            'available': [profile.strip().split()[1] for profile in all_profiles]
        }
    }

@facts.command()
def gcc():
    """The current profile"""
    pprint.pprint(fact())
    return 0
