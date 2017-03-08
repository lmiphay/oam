# -*- coding: utf-8 -*-

import logging
from invoke import task
import merge

@task
def newuse(ctx, env='OAM_TAG=newuse'):
    merge.emerge(ctx, opts='--update --newuse --deep --with-bdeps=y', target='world', tag=env)

@task
def depclean(ctx, env='OAM_TAG=depclean'):
    merge.emerge(ctx, opts='--pretend --depclean', target='world', tag=env)

@task(default=True, pre=[newuse, depclean])
def all(ctx):
    logging.info('depclean done')
