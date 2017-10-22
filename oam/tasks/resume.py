# -*- coding: utf-8 -*-

from __future__ import print_function
import json
import os
import pprint
import re
import shutil
import yaml

from invoke import task

from oam.daylog import last_day

MTIMEDB = '/var/cache/edb/mtimedb'
OAM_CACHE_MTIMEDB = '/var/cache/oam/mtimedb'
OAM_LOGDIR ='/var/log/oam'

@task
def save(ctx):
    """Create a timestamped backup of the current resume list"""
    if not os.path.exists(OAM_CACHE_MTIMEDB):
        os.makedirs(OAM_CACHE_MTIMEDB)
    shutil.copy2(MTIMEDB, '{}/{}'.format(OAM_CACHE_MTIMEDB,
                                         os.path.getmtime(MTIMEDB)))

@task(default=True, pre=[save])
def resume(ctx, extraopt='', env={}):
    """resume the last interrupted merge; extraopt=--skipfirst"""
    ctx.emerge('--resume {extraopt}'.format(extraopt=extraopt),
               env=env)

@task(pre=[save])
def clean(ctx):
    """remove old resume settings from mtimedb (archive it off first)"""
    ctx.run('emaint --fix cleanresume')

def mergelist(record):
    """dump the mtimedb resume list in a format suitable for feeding back into emerge"""
    for rec in record:
        print('={}'.format(rec[2]))

def show_record(mtimedb, key):
    """dump the specified record if it exists in mtimedb"""
    if key in mtimedb:
        print('--- {}'.format(key))
        mergelist(mtimedb[key])
        pprint.pprint(mtimedb[key])

# see: https://github.com/gentoo/portage/blob/master/pym/portage/util/mtimedb.py
# import portage.util.mtimedb
@task
def show(ctx):
    """dump the list of ebuilds from the resume record(s) in mtimedb"""
    mtimedb = json.loads(open(MTIMEDB).read())
    for key in ['resume', 'resume_backup']:
        show_record(mtimedb, key)

@task
def record(ctx, daydir=last_day()):
    """save a copy of mtimedb to the /var/log/oam/[daydir] in yaml format"""
    yaml.dump(json.loads(open(MTIMEDB).read()),
              open('{}/{}/mtimedb-{}.yaml'.format(OAM_LOGDIR, daydir, os.path.getmtime(MTIMEDB)), 'w'),
              default_flow_style=False))
