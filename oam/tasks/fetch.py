# -*- coding: utf-8 -*-

import logging
from invoke import task, call
import merge

@task
def fetchonly(ctx, env='OAM_TAG=fetch'):
    merge.emerge(ctx, opts='--fetchonly --update', target='world', tag=env)

@task(default=True, pre=[fetchonly])
def all(ctx):
    logging.info('empty tree emerge done')
