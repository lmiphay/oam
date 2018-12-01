# -*- coding: utf-8 -*-

import os
from invoke import task


@task
def qt(ctx):
    ctx.run("emerge -v1 $(equery -q list --format='$cp' dev-qt/*)")

@task
def kde_frameworks(ctx):
    ctx.run("emerge -v1 $(equery -q list --format='$cp' kde-frameworks/*)")

@task
def plasma(ctx):
    ctx.run("emerge -v1 $(equery -q list --format='$cp' kde-plasma/*)")

@task
def kde_apps(ctx):
    ctx.run("emerge -v1 $(equery -q list --format='$cp' kde-apps/*)")

@task
def kde_misc(ctx):
    ctx.run("emerge -v1 $(equery -q list --format='$cp' kde-misc/*)")

@task(pre=[qt,kde_frameworks,plasma,kde_apps,kde_misc])
def kde(ctx):
    pass
