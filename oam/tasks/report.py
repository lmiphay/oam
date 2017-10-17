# -*- coding: utf-8 -*-

import os
from invoke import task

from oam.daylog import last_day
import oam.facts
from oam.report import Report
import oam.settings
import oam.tasks.config

@task
def facts(ctx, daydir=last_day()):
    context = oam.facts.get_facts(daydir)
    context.update(oam.tasks.config.profiles(ctx))
    return context

@task
def write(ctx, context, out_filename='summary.log', template='summary.jinja2'):
    with open(out_filename, 'w') as summary:
        summary.write(Report(context).render(template))

# daydir should be similar to: 20160403 
@task(default=True)
def report(ctx, daydir=last_day()):
    logdir = oam.settings.oam.logs.directory  # e.g. /var/log/oam
    curdir = os.getcwd()
    try:
        os.chdir('{}/{}'.format(logdir, daydir))
        write(ctx, facts(ctx, daydir))
    finally:
        os.chdir(curdir)
