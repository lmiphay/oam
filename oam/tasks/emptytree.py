# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import re

from invoke import task
from invoke.tasks import call

from oam.tasks.config import is_latest
import oam.tasks.resume

EMPTYTREE_ENV = {'I_KNOW_WHAT_I_AM_DOING': '1'}


@task(pre=[call(is_latest, profile='gcc'), call(is_latest, profile='binutils')])
def check(ctx):
    print('pre-checks done')

@task(check)
def system(ctx):
    """rebuild the system packages (twice for luck)"""
    for i in range(2):
        ctx.emerge('@system')

@task(default=True, pre=[check])
def emptytree(ctx, extraopt=''):
    """reinstall world and its 'entire dependency tree'"""
    ctx.emerge('--keep-going --emptytree {extraopt} world'.format(extraopt=extraopt),
               env=EMPTYTREE_ENV)

@task
def resume(ctx, extraopt=''):
    """resume an interrupted emptytree world merge"""
    oam.tasks.resume.resume(ctx, extraopt=extraopt, env=EMPTYTREE_ENV)

@task(pre=[call(emptytree, extraopt='--pretend')])
def manifest(ctx):
    """list packages to be built by an emptytree merge"""
    pass
