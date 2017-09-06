# -*- coding: utf-8 -*-

from invoke import task

import oam.daylog
import oam.facts
import oam.report
import oam.settings

@task(default=True)
def report(ctx):
    logdir = oam.settings.oam.logs.dir # /var/log/oam
    daydir = oam.daylog.last_day()     # 20160403
    with ctx.cd('{}/{}'.format(logdir, daydir)):
        oam.facts.write_facts(daydir, 'summary.yaml')
        with open('summary.log', 'w') as summary:
            summary.write(oam.report.Report().build(['summary.yaml']).render('summary.jinja2'))
