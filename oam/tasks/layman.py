# -*- coding: utf-8 -*-

import logging
from invoke import task

# check: layman spams the error log
@task
def layman(ctx):
    ctx.run('layman --sync=ALL --nocolor')

@task(layman)
def all(ctx):
    logging.info('layman sync done')
