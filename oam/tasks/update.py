# -*- coding: utf-8 -*-

import logging
from invoke import task
import merge

@task(name='update-package')
def update_package(ctx, atom='sys-apps/portage'):
    if is_update_available(atom):
        merge.emerge(ctx, opts='--oneshot', target=atom)

@task(name='revdep-rebuild')
def revdep_rebuild(ctx):
    if check_for_executable('/usr/bin/revdep-rebuild'):
        ctx.run('/usr/bin/revdep-rebuild --nocolor --ignore')

@task(name='python-updater')
def python_updater(ctx):
    if check_for_executable('/usr/sbin/python-updater'):
        ctx.run('/usr/sbin/python-updater -eall')

@task(name='perl-cleaner')
def perl_cleaner(ctx):
    if check_for_executable('/usr/sbin/perl-cleaner'):
        ctx.run('/usr/sbin/perl-cleaner -all')
    
@task(name='preserved-rebuild')
def preserved_rebuild(ctx):
    if len(preserved_libs())>0:
        merge.emerge(ctx, opts='--keep-going', target='@preserved-rebuild')

@task
def update(ctx):
    merge.emerge(ctx, opts='--update --keep-going', target='world')

@task(default=True, pre=[update_package, update, revdep_rebuild, python_updater, perl_cleaner, preserved_rebuild])
def all(ctx):
    logging.info('update done')
