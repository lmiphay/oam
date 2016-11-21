#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import pprint
import time
import click
import importlib
import yaml
from .cmd import cli
from oam.daylog import last_day

FACT = [
    'oam.fact.blocks',
    'oam.fact.checkconfig',
    'oam.fact.downgrades',
    'oam.fact.kernbuilt',
    'oam.fact.logdate',
    'oam.fact.merges',
    'oam.fact.obsolete',
    'oam.fact.profile',
    'oam.fact.qcheckdiff',
    'oam.fact.runs',
    'oam.fact.server',
    'oam.fact.synchistory',
    'oam.fact.unreadnews'
]
FACTMOD = []

def import_facts():
    global FACTMOD
    FACTMOD = map(importlib.import_module, FACT)

def get_facts(day):
    if len(FACTMOD) == 0:
        import_facts()

    result = {'timestamp': time.strftime('%Y%m%d:%H:%M:%S') }
    for mod in FACTMOD:
        result.update(mod.fact(day))

    return result

def write_facts(day, outfile):
    yaml.dump(get_facts(day), open(outfile, 'w'), default_flow_style=False)

@cli.group(invoke_without_command=True)
@click.option('--day', default=last_day(), help='day logs to process')
@click.option('--outfile', help='write facts to file')
def facts(day, outfile):
    """Server/build information"""
    if outfile:
        write_facts(day, outfile)
    else:
        print(pprint.pformat(get_facts(day)))
    return 0
