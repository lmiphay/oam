# -*- coding: utf-8 -*-

from invoke import task

@task(default=True)
def skel(ctx):
    ctx.run('echo hello world')
