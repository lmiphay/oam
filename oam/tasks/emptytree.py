# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import re

from invoke import task

@task
def setup(ctx):
    ctx.gcc = {}

@task(setup)
def gcc_current(ctx):
    ctx.gcc.current = ctx.run('gcc-config -c', hide='out').stdout.strip()

@task(setup)
def gcc_latest(ctx):
    ctx.gcc.latest = ctx.run("gcc-config -l -C | tail -1 | awk '{print $2}'", hide='out').stdout.strip()

@task(gcc_current, gcc_latest)
def gcc_current_is_latest(ctx, gcc_version_check=True):
    """force an error unless the currently selected gcc is not the newest version installed"""
    if gcc_version_check and (ctx.gcc.current != ctx.gcc.latest):
        raise RuntimeError('current gcc ({}) is not the latest installed({})'.format(ctx.gcc.current, ctx.gcc.latest))

@task(gcc_current_is_latest)
def system(ctx):
    """rebuild the system packages (twice for luck)"""
    for i in range(2):
        ctx.emerge('@system')

@task(default=True, pre=[gcc_current_is_latest])
def emptytree(ctx, extraopt=''):
    """rebuild everything in world and needed by it"""
    ctx.emerge('--keep-going --emptytree {extraopt} world',
               extraopt=extraopt,
               env={'I_KNOW_WHAT_I_AM_DOING': '1'})

def emergelog_current():
    return os.stat('/var/log/emerge.log').st_size

@task
def manifest(ctx):
    """generate a list of packages which would be build for an emptytree rebuild"""
    print('emergelog_current {}'.format(emergelog_current))
    emptytree(ctx, '--pretend')

# 1506776832:  ::: completed emerge (43 of 44) sys-fs/e2fsprogs-1.43.3-r1 to /
MERGE_RECORD = r'(\d+)::  ::: completed emerge \(\d+ of \d+\) ([-\w\d\.]+) to '
