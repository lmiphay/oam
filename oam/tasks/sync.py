# -*- coding: utf-8 -*-

import os
from invoke import task


@task(name='eix-update')
def eix_update(ctx):
    """Update the local eix db after a sync (otherwise eix is broken)"""
    ctx.run('eix-update --nocolor')

@task(name='eix-remote')
def eix_remote(ctx):
    """Fetch the eix db's and add to eix db"""
    ctx.run('eix-remote -H update1')  # -H = "Suppress status line update"
    # ctx.run('eix-remote add1')

@task
def eix(ctx):
    """Run eix-update and eix-remote if they are installed"""
    if os.path.exists('/usr/bin/eix-update'):
        eix_update(ctx)
        if os.path.exists('/usr/bin/eix-remote'):
            eix_remote(ctx)

# TODO: add warnings to report
@task
def check(ctx):
    """This tends to return non zero results..."""
    ctx.run('emaint --check all')

@task(default=True, post=[eix])
def sync(ctx):
    """Sync repos which have their auto-sync setting set to true"""
    ctx.run('emaint --auto sync')
