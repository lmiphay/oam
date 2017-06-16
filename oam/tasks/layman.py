# -*- coding: utf-8 -*-

from invoke import task

# check: layman spams the error log
@task(default=True)
def layman(ctx):
    ctx.run('layman --sync=ALL --nocolor')
