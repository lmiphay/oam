# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
import logging
import pprint
import click
from oam.facts import facts

CURRENT_COMMAND = 'eselect python show'
LIST_COMMAND = 'eselect python list'

def fact(day=None):
    """Return python profile information"""
    current = subprocess.check_output(CURRENT_COMMAND, shell=True).decode('utf-8').splitlines()[0].strip()
    all_profiles = subprocess.check_output(LIST_COMMAND, shell=True).decode('utf-8').splitlines()

    return {
        'python': {
            'current': current,
            'available': [profile.strip().split()[1] for profile in all_profiles]
        }
    }

@facts.command()
def python():
    """The current profile"""
    pprint.pprint(fact())
    return 0
