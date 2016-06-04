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
from .merges import Merges
from .blocks import Blocks
from .daylog import DayLog, last_day

DEFAULT_TEMPLATE = 'txt_summary.template'
TEMPLATE_DIR = '/usr/share/gentoo-oam'

def profile():
    """Return the current gentoo profile"""
    return subprocess.check_output('eselect profile show',
                                   shell=True).splitlines()[1].strip()

LAST_SYNC = '/usr/portage/metadata/timestamp.chk'

def last_sync():
    """Should be moved to part of the update action and stored at that point"""
    if os.path.exists(LAST_SYNC):
        return open(LAST_SYNC, 'r').read().strip()
    else:
        return 'Unknown'

def server_context():
    return {
        'hostname':os.uname()[1],
        'profile': profile(),
        'last_sync': last_sync()
        }

""" Generate a report on oam merge activities
"""
class Summary(object):

    def __init__(self, daydir):
        self.day = DayLog(daydir)
        self.context = {}

    def save(self, filename):
        yaml.dump(self.context, open(filename, 'w'), default_flow_style=False)

    def load(self, filename):
        self.context = yaml.load(self.context)
        return self

    def build(self):
        """Build a context for subsequent rendering"""
        self.context['server'] = server_context()
        self.context['merges'] = Merges.run(self.day.runfiles('merge.log')).context()
        self.context['blocks'] = Blocks.run(self.day.runfiles('blocks.log')).context()
        return self

    def render(self, template):
        loader=jinja2.FileSystemLoader([os.path.dirname(template), TEMPLATE_DIR])
        env = jinja2.Environment(loader)
        return env.get_template(os.path.basename(template)).render(self.context)

@cli.command()
@click.option('--template', default=DEFAULT_TEMPLATE, envvar='OAM_SUMMARY_TEMPLATE')
@click.option('--daydir', default=last_day())
def summary(template, daydir):
    """Summarise blocks/merge-failures"""
    print(Summary(daydir).build().render(template))
    return 0
