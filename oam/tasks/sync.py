# -*- coding: utf-8 -*-

import logging
from invoke import task
import merge

@task
def sync(ctx):
    ctx.run('emaint --auto sync')

@task(name='eix-update')
def eix_update(ctx):
    ctx.run('eix-update --nocolor')

@task(name='eix-remote')
def eix_remote(ctx):
    ctx.run('eix-remote -H update1')
    # ctx.run('eix-remote add1')

@task(sync, eix_update, eix_remote)
def all(ctx):
    logging.info('sync done')
