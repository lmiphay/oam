# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
import logging
import pprint
import click
from oam.facts import facts

CURRENT_COMMAND = 'eselect binutils show'
LIST_COMMAND = 'eselect binutils list'

def fact(day=None):
    """Return binutils profile information"""
    current = subprocess.check_output(CURRENT_COMMAND, shell=True).splitlines()[0].strip()
    all_profiles = subprocess.check_output(LIST_COMMAND, shell=True).splitlines()

    return {
        'binutils': {
            'current': current,
            'available': [profile.strip().split()[1] for profile in all_profiles]
        }
    }

@facts.command()
def binutils():
    """binutils profile information"""
    pprint.pprint(fact())
    return 0
