# -*- coding: utf-8 -*-

import logging
from invoke import task, call
import merge

@task
def system(ctx, env='OAM_TAG=system'):
    merge.emerge(ctx, target='@system', tag=env)

@task
def emptytree(ctx, env='I_KNOW_WHAT_I_AM_DOING=1 OAM_TAG=emptytree'):
    merge.emerge(ctx, opts='--emptytree', target='world', tag=env)

FULL_BUILD = [
    call(system, 'OAM_TAG=system_1'),
    call(system, 'OAM_TAG=system_2'),
    emptytree
]

@task(default=True, pre=FULL_BUILD)
def all(ctx):
    logging.info('empty tree emerge done')
