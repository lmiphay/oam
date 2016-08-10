#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess
import logging
import click
from oam.facts import facts

COMMAND = 'eselect profile show'

def fact(day=None):
    """Return the current gentoo profile"""
    output = subprocess.check_output(COMMAND, shell=True).splitlines()
    if len(output) == 2:
        return { 'profile': output[1].lstrip() }
    else:
        logging.error('failed read current profile: %s', str(output))
        return { 'profile': 'unknown' }

@facts.command()
def profile():
    """The current gentoo profile"""
    print(fact()['profile'])
    return 0
