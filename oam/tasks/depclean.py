# -*- coding: utf-8 -*-

from __future__ import print_function
import sys

from invoke import task

@task
def newuse(ctx):
    """bring the system up-to-date prior to a depclean run"""
    ctx.emerge('--update --newuse --deep --with-bdeps=y world')

@task(default=True, pre=[newuse])
def pretend(ctx):
    """list packages that would be removed"""
    ctx.emerge('--pretend --depclean world')

@task(aliases=['format'])
def reformat(ctx, deps='-'):
    """re-format the output of 'emerge --pretend --depclean world'"""
    for line in sys.stdin if deps=='-' else open(deps).readlines():
        if 'All selected packages:' in line:
            for atom in sorted(line.replace('All selected packages:', '').split()):
                print('={}'.format(atom))

@task
def add(ctx, atom):
    """add package to the world file with rebuilding it"""
    ctx.emerge('--noreplace {}'.format(atom))
