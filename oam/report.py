#!/usr/bin/python

from __future__ import print_function
import sys
import os
import re
import subprocess
import yaml
import jinja2
import click
from .cmd import cli

TEMPLATE_DIR = '/usr/share/gentoo-oam'

""" Generate a report
"""
class Report(object):

    def __init__(self):
        self.context = {}

    def load(self, filename):
        self.context.update(yaml.load(open(filename, 'r')))
        return self

    def build(self, factfiles):
        """Build a context for subsequent rendering"""
        for ff in factfiles:
            self.load(ff)
        return self

    def render(self, template):
        env = jinja2.Environment()
        env.loader = jinja2.FileSystemLoader([os.path.dirname(template), TEMPLATE_DIR])
        return env.get_template(os.path.basename(template)).render(self.context)

@cli.command()
@click.argument('template')
@click.argument('factfiles', nargs=-1)
def report(template, factfiles):
    """Generate a server report"""
    print(Report().build(factfiles).render(template))
    return 0
