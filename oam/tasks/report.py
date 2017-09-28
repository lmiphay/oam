# -*- coding: utf-8 -*-

import os
from invoke import task

from oam.daylog import last_day
import oam.facts
from oam.report import Report
import oam.settings

# daydir should be similar to: 20160403 
@task(default=True)
def report(ctx, daydir=last_day()):
    logdir = oam.settings.oam.logs.directory  # e.g. /var/log/oam
    curdir = os.getcwd()
    try:
        os.chdir('{}/{}'.format(logdir, daydir))
        oam.facts.write_facts(daydir, 'summary.yaml')
        with open('summary.log', 'w') as summary:
            summary.write(Report().build(['summary.yaml']).render('summary.jinja2'))
    finally:
        os.chdir(curdir)
