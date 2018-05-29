# -*- coding: utf-8 -*-

import os
from invoke import task

import jinja2
import markdown
import markdown.extensions.tables

from oam.daylog import last_day
import oam.facts
from oam.report import Report
import oam.settings
import oam.tasks.config

@task
def facts(ctx, daydir=None):
    if not daydir:
        daydir = last_day()
    context = oam.facts.get_facts(daydir)
    context.update(oam.tasks.config.profiles(ctx))
    return context

@task
def write(ctx, context, out_filename='summary.log', template='summary.jinja2'):
    with open(out_filename, 'w') as summary:
        summary.write(Report(context).render(template))

# daydir should be similar to: 20160403 
@task(default=True)
def report(ctx, daydir=None):
    if not daydir:
        daydir = last_day()
    logdir = oam.settings.oam.logs.directory  # e.g. /var/log/oam
    curdir = os.getcwd()
    try:
        os.chdir('{}/{}'.format(logdir, daydir))
        write(ctx, facts(ctx, daydir))
    finally:
        os.chdir(curdir)

@task
def fancy(ctx):
    context = facts(ctx)
    md = jinja2.Template(open('/usr/share/oam/summary-md.jinja2', 'r').read()).render(context)
    with open('/var/log/oam/{}/summary.html'.format(last_day()), 'w') as html:
        html.write(markdown.markdown(md, extensions=[markdown.extensions.tables.TableExtension()]))

