# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import re
import yaml

from invoke import task

TOOLS = [
    'binutils'
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
def current_is_latest(ctx, profile='gcc', version_check=True):
    """check if the current profile is the latest installed.
       optionally raise an exception if its not.
    """
    if current(ctx, profile) == latest(ctx, profile):
        return True
    else:
        if version_check:
            raise RuntimeError('current {profile} is not the latest installed'.format(profile=profile))
        return False

@task
def show(ctx, profile='gcc'):
    """show the current and and latest available profiles"""
    print(current(ctx, profile), latest(ctx, profile))

@task
def profiles(ctx, profile='gcc'):
    """dump the currently selected and available profiles"""
    config = {}
    for tool in TOOLS:
        config[tool] = {}
        config[tool]['current'] = current(ctx, tool)
        config[tool]['latest'] = latest(ctx, tool)
        config[tool]['is_latest'] = current_is_latest(ctx, tool, version_check=False)
        config[tool]['available'] = available(ctx, tool)
    print(yaml.dump({'config': config}, default_flow_style=False))
