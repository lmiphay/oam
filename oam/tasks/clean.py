# -*- coding: utf-8 -*-

import logging

from invoke import task

@task
def distfiles(ctx, enabled=True):
    if enabled:
        ctx.run('eclean --nocolor distfiles')

@task
def kernel(ctx, enabled=False):
    if enabled:
        ctx.run('eclean-kernel --num=3 --exclude=config --no-mount')

@task(default=True, pre=[distfiles, kernel])
def all(ctx):
    logging.info('clean up done')
