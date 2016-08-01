#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import pprint
import time
import click
import importlib
import yaml
from .cmd import cli

FACT = [
    'oam.fact.blocks',
    'oam.fact.logdate',
    'oam.fact.merges',
    'oam.fact.profile',
    'oam.fact.runs',
    'oam.fact.server',
    'oam.fact.synchistory'
]
FACTMOD = []

def import_facts():
    global FACTMOD
    FACTMOD = map(importlib.import_module, FACT)

def get_facts():
    if len(FACTMOD) == 0:
        import_facts()

    result = {'timestamp': time.strftime('%Y%m%d:%H:%M:%S') }
    for mod in FACTMOD:
        result.update(mod.fact())

    return result

@cli.group(invoke_without_command=True)
@click.option('--outfile', help='write facts to file')
def facts(outfile):
    """Server/build information"""
    if outfile:
        yaml.dump(get_facts(), open(outfile, 'w'), default_flow_style=False)
    else:
        print(pprint.pformat(get_facts()))
    return 0
