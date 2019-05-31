# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import logging
import yaml
import jinja2
import click
from .cmd import cli

TEMPLATE_DIR = '/usr/share/oam'
DEFAULT_TEMPLATE = 'summary.jinja2'

""" Generate a report
"""
class Report(object):

    def __init__(self, context={}):
        self.logger = logging.getLogger("oam.report")
        self.context = context

    def load(self, filename):
        self.context.update(yaml.safe_load(open(filename, 'r')))
        return self

    def build(self, factfiles):
        """Build a context for subsequent rendering"""
        for filename in factfiles:
            if os.path.exists(filename):
                self.load(filename)
            else:
                self.logger.log(logging.ERROR, '%s is missing', filename)
        return self

    def render(self, template=DEFAULT_TEMPLATE):
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
