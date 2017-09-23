# -*- coding: utf-8 -*-

from invoke import task

import oam.daylog
import oam.facts
import oam.report
import oam.settings

# daydir should be similar to: 20160403 
@task(default=True)
def report(ctx, daydir=oam.daylog.last_day())
    logdir = oam.settings.oam.logs.directory  # e.g. /var/log/oam

    with ctx.cd('{}/{}'.format(logdir, daydir)):
        oam.facts.write_facts(daydir, 'summary.yaml')
        with open('summary.log', 'w') as summary:
            summary.write(oam.report.Report().build(['summary.yaml']).render('summary.jinja2'))
