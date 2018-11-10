# -*- coding: utf-8 -*-

from __future__ import print_function
import pprint
import time
import click
import importlib
import yaml

from oam.cmd import cli
from oam.daylog import last_day


FACT = [
    'oam.fact.binutils',
    'oam.fact.blocks',
    'oam.fact.checkconfig',
    'oam.fact.downgrades',
    'oam.fact.gcc',
    'oam.fact.kernbuilt',
    'oam.fact.logdate',
    'oam.fact.merges',
    'oam.fact.obsolete',
    'oam.fact.portageinfo',
    'oam.fact.profile',
    'oam.fact.python',
    'oam.fact.qcheckdiff',
    'oam.fact.runs',
    'oam.fact.server',
    'oam.fact.synchistory',
    'oam.fact.unreadnews'
]


def get_facts(day):
    factmod = [importlib.import_module(name) for name in FACT]
    
    result = {'timestamp': time.strftime('%Y%m%d:%H:%M:%S') }

    for mod in factmod:
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
