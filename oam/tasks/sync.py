# -*- coding: utf-8 -*-

from invoke import task

@task(name='eix-update')
def eix_update(ctx):
    """Update the local eix db after a sync (otherwise eix is broken)"""
    ctx.run('eix-update --nocolor')

@task(name='eix-remote')
def eix_remote(ctx):
    ctx.run('eix-remote -H update1')
    # ctx.run('eix-remote add1')

@task(default=True, post=[eix_update, eix_remote])
def sync(ctx):
    """Sync repos which have their auto-sync setting set to true"""
    ctx.run('emaint --auto sync')
