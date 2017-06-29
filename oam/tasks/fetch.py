# -*- coding: utf-8 -*-

from invoke import task

@task(default=True, aliases=['fetchonly'])
def fetch(ctx):
    ctx.emerge('--fetchonly --update world')
