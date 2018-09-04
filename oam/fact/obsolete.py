# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import click

from oam.facts import facts
from oam.obsolete import Obsolete

def fact(day=None):
    """Return a list of obsolete items under /etc/portage"""
    return {
        'obsolete': [ x for x in Obsolete().its() ]
    }

@facts.command()
def obsolete():
    """Print list of obsolete items"""
    print(fact()['obsolete'])
    return 0
