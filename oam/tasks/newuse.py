# -*- coding: utf-8 -*-

from invoke import task

@task(default=True)
def newuse(ctx):
    ctx.emerge('--newuse --update world')
