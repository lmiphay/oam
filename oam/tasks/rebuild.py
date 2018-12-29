# -*- coding: utf-8 -*-

import os
from invoke import task

REBUILD = "emerge -v1 $(equery -q list --format='$cp' {}/*)"

@task
def x11_libs(ctx):
    ctx.run(REBUILD.format('x11-libs'))

@task
def x11_base(ctx):
    ctx.run(REBUILD.format('x11-base'))

@task
def x11_drivers(ctx):
    ctx.run(REBUILD.format('x11-drivers'))

@task(x11_libs,x11_base,x11_drivers)
def x11(ctx):
    pass

@task
def qt(ctx):
    ctx.run(REBUILD.format('dev-qt'))

@task
def kde_frameworks(ctx):
    ctx.run(REBUILD.format('kde-frameworks'))

@task
def plasma(ctx):
    ctx.run(REBUILD.format('kde-plasma'))

@task
def kde_apps(ctx):
    ctx.run(REBUILD.format('kde-apps'))

@task
def kde_misc(ctx):
    ctx.run(REBUILD.format('kde-misc'))

@task(pre=[qt,kde_frameworks,plasma,kde_apps,kde_misc])
def kde(ctx):
    pass

@task(x11,kde)
def all(ctx):
    pass
