# -*- coding: utf-8 -*-

from __future__ import print_function

import yaml
import click
from .cmd import cli
from oam.daylog import last_day
from oam.facts import get_facts
from oam.report import Report

class Status(object):

    def __init__(self, day, yaml_format):
        self.day = day
        self.yaml_format = yaml_format

    def run(self):
        if self.yaml_format:
            return yaml.dump(get_facts(self.day), default_flow_style=False)
        else:
            return Report(get_facts(self.day)).render()

@cli.command()
@click.option('--day', default=last_day(), help='day logs to process')
@click.option('--yaml-format', is_flag=True, help='return status as yaml')
def status(day, yaml_format):
    """Generate an on the fly status report for the server"""
    print(Status(day, yaml_format).run())
    return 0

