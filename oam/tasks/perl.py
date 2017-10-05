# -*- coding: utf-8 -*-

from __future__ import print_function
from invoke import task

@task
def update(ctx):
    """see: https://wiki.gentoo.org/wiki/Perl#Upgrading_.28major_version.29"""
    ctx.run('emerge -uDNav --with-bdeps=y --backtrack=100 --autounmask-keep-masks=y @world')

@task
def cleaner(ctx):
    ctx.run('/usr/sbin/perl-cleaner --all')

@task(update,cleaner)
def major(ctx):
    ctx.run('perl --version')
