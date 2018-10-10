# -*- coding: utf-8 -*-

from invoke import task

# todo: optionally wipe /var/tmp/portage?, packages... etc

@task(default=True)
def distfiles(ctx):
    ctx.run('eclean --nocolor distfiles')

@task
def kernel(ctx):
    ctx.run('eclean-kernel --num=3 --exclude=config --no-mount')
