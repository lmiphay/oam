#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import pprint
import click
import importlib
from .cmd import cli

FACT = ['oam.fact.profile', 'oam.fact.server', 'oam.fact.synchistory']
FACTMOD = []

def import_facts():
    global FACTMOD
    FACTMOD = map(importlib.import_module, FACT)

def get_facts():
    if len(FACTMOD) == 0:
        import_facts()

    result = {}
    for mod in FACTMOD:
        result.update(mod.fact())

    return result

@cli.group(invoke_without_command=True)
def facts():
    """Server/build information"""
    print(pprint.pformat(get_facts()))
