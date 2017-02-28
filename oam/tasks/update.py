# -*- coding: utf-8 -*-

from invoke import task
from oam.options import oam_config

@task(name='update-package')
def update_package(ctx, atom='sys-apps/portage'):
    if is_update_available(atom):
        ctx.run('/usr/bin/emerge --oneshot --verbose --verbose-conflicts {}'.format(atom))

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
        ctx.run('/usr/bin/emerge --keep-going --verbose @preserved-rebuild')
        
@task
def emerge(ctx, options=oam_config('emerge_opts'), target='--update world'):
    ctx.run('/usr/bin/emerge {} {}'.format(options, target))
        
@task(default=True, pre=[update_package], post=[revdep_rebuild, python_updater, perl_cleaner, preserved_rebuild])
def update(ctx):
    ctx.run('/usr/bin/emerge --update --keep-going {} world'.format(oam_config('emerge_opts')))
