# -*- coding: utf-8 -*-

import logging
from invoke import task
import merge

@task
def newuse(ctx, env='OAM_TAG=newuse'):
    merge.emerge(ctx, opts='--newuse --update', target='world', tag=env)

@task(newuse)
def all(ctx):
    logging.info('newuse done')
