#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import click

from oam.facts import facts
from oam.checkconfig import CheckConfig

def fact(day=None):
    """Return a list configuration problems"""
    return {
        'check_config': [ x for x in CheckConfig().its() ]
    }

@facts.command()
def checkconfig():
    """Print list of configuration problems"""
    print(fact()['check_config'])
    return 0
