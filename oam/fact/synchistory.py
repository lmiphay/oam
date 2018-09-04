# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import click
from oam.facts import facts

LAST_SYNC = '/usr/portage/metadata/timestamp.chk'

def fact(day=None):
    """Return the time/date of the last portage sync"""
    if os.path.exists(LAST_SYNC):
        return { 'lastsync': open(LAST_SYNC, 'r').read().strip() }
    else:
        return { 'lastsync': 'unknown' }

@facts.command()
def synchistory():
    """The time/date of the last portage sync"""
    print(fact()['lastsync'])
    return 0
