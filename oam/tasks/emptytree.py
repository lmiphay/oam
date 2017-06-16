# -*- coding: utf-8 -*-

from invoke import task, call

@task
def system(ctx):
    for i in range(2):
        ctx.emerge('@system')

@task(default=True)
def emptytree(ctx):
    ctx.emerge('--emptytree world', env={'I_KNOW_WHAT_I_AM_DOING': '1'})
