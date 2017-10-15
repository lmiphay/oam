# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import re
import sys
import yaml

from invoke import task

TOOLS = [
    'binutils' # also available as 'eselect binutils list'
    ,'gcc'
]

# current binutils-config does not support --nocolor

@task
def read(ctx, profile='gcc', opts='--list-profiles --nocolor'):
    """run the specified profile config program returning the program output"""
    return str(ctx.run('{profile}-config {opts}'.format(profile=profile, opts=opts),
                       hide='out').stdout.rstrip())

@task
def current(ctx, profile='gcc'):
    """return the currently selected profile"""
    return read(ctx, profile, '--get-current-profile')

@task
def available(ctx, profile='gcc'):
    """return the available profiles"""
    return [line.strip().split(' ')[1] for line in read(ctx, profile, '--list-profiles').split('\n')]

@task
def latest(ctx, profile='gcc'):
    """return the latest profile installed"""
    return available(ctx, profile)[-1]

@task
def is_latest(ctx, profile='gcc'):
    """check if the current profile is the latest installed"""
    return current(ctx, profile) == latest(ctx, profile)

@task
def require_latest(ctx, profile='gcc'):
    """raise an exception if the current profile is the latest installed"""
    if not is_latest(ctx, profile):
        raise RuntimeError('current {profile} is not the latest installed'.format(profile=profile))

ATTRIBUTES = ['current', 'latest', 'is_latest', 'available']

@task
def profiles(ctx):
    """return the currently selected and available profiles"""
    result = {}
    for tool in TOOLS:
        result[tool] = {key: globals()[key](ctx, tool) for key in ATTRIBUTES}
    return {'config': result}

@task(default=True)
def show(ctx):
    """show the current and latest available profiles"""
    print(yaml.dump(profiles(ctx), default_flow_style=False))
