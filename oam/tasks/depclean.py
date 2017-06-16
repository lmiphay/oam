# -*- coding: utf-8 -*-

from invoke import task

@task
def newuse(ctx):
    ctx.emerge('--update --newuse --deep --with-bdeps=y world')

@task(default=True, pre=[newuse])
def depclean(ctx):
    ctx.emerge('--pretend --depclean world')
