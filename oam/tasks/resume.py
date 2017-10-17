# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import os
import pprint
import re

from invoke import task

MTIMEDB = '/var/cache/edb/mtimedb'

@task(default=True)
def resume(ctx, extraopt='', env={}):
    """resume the last interrupted merge; extraopt=--skipfirst"""
    ctx.emerge('--resume {extraopt}'.format(extraopt=extraopt),
               env=env)

@task
def clean(ctx):
    """remove old resume settings from mtimedb"""
    ctx.run('emaint --fix cleanresume')

# see: https://github.com/gentoo/portage/blob/master/pym/portage/util/mtimedb.py
# import portage.util.mtimedb
@task
def show(ctx):
    """dump the resume_backup record from mtimedb"""
    mtimedb = json.loads(open(MTIMEDB).read())
    pprint.pprint(mtimedb['resume_backup'])
