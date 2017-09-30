# -*- coding: utf-8 -*-

from invoke import task

@task
def setup(ctx):
    ctx.gcc = {}

@task(setup)
def gcc_current(ctx):
    ctx.gcc.current = ctx.run('gcc-config -c', hide='out').stdout.strip()

@task(setup)
def gcc_latest(ctx):
    ctx.gcc.latest = ctx.run("gcc-config -l -C | tail -1 | awk '{print $2}'", hide='out').stdout.strip()

@task(gcc_current, gcc_latest)
def gcc_current_is_latest(ctx, gcc_version_check=True):
    if gcc_version_check and (ctx.gcc.current != ctx.gcc.latest):
        raise RuntimeError('current gcc ({}) is not the latest installed({})'.format(ctx.gcc.current, ctx.gcc.latest))

@task(gcc_current_is_latest)
def system(ctx):
    for i in range(2):
        ctx.emerge('@system')

@task(default=True, pre=[gcc_current_is_latest])
def emptytree(ctx):
    ctx.emerge('--keep-going --emptytree world', env={'I_KNOW_WHAT_I_AM_DOING': '1'})
