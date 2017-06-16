# -*- coding: utf-8 -*-

from invoke import task

@task(default=True)
def sync(ctx):
    """Sync repos which have their auto-sync setting set to true"""
    ctx.run('emaint --auto sync')
