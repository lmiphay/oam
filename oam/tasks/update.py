# -*- coding: utf-8 -*-

from invoke import task
import oam.lib

""" Todo:
    strip ansi for perl-cleaner
    need regex filtering for perl-cleaner
    add changed python and perl installs
    note: revdep-rebuild and perl-cleaner have pretend support
    note: `emerge --rebuild-if-new-rev=y` doesn't appear to be useful for update pkg
"""

@task(name='update-available')
def update_available(ctx):
    with ctx.cd('/var/log/oam/latest'):
        return ctx.run("tail -n 7 sync.log | grep -q 'An update to portage is available'").ok

@task(name='update-package', aliases=['update-portage'])
def update_package(ctx, atom='sys-apps/portage'):
    ctx.emerge('--oneshot {}'.format(atom), if_new_rev=True)

@task(name='revdep-rebuild', aliases=['rr'])
def revdep_rebuild(ctx):
    ctx.run('/usr/bin/revdep-rebuild --nocolor --ignore', if_installed=True)

@task(name='python-updater', aliases=['pu'])
def python_updater(ctx):
    """overkill(?) from https://wiki.gentoo.org/wiki/Python#Version_upgrade"""
    ctx.run('emerge --ask --update --newuse --deep @world')
    ctx.run('emerge --ask --changed-use --deep @world')
    ctx.run('emerge --ask --depclean dev-lang/python')

@task(name='perl-cleaner', aliases=['pc'])
def perl_cleaner(ctx):
    ctx.run('/usr/sbin/perl-cleaner --all', if_installed=True)
    
@task(name='preserved-rebuild', aliases=['pr'])
def preserved_rebuild(ctx, force=False):
    if force or oam.lib.preserved_libs():
        ctx.emerge('--keep-going @preserved-rebuild')

PRE = [update_package]
POST = [revdep_rebuild, perl_cleaner, preserved_rebuild]

@task(default=True, pre=PRE, post=POST, aliases=['up'])
def update(ctx, target='world'):
    """
    note that if a problem is found in the pretend phase, then --keep-going
    will not keep the build running (the pre-merge check will fail the update)

    wiki:
       --newuse and/or --changed-use from: https://wiki.gentoo.org/wiki/Python#Version_upgrade
       --newuse: include installed packages where USE flags have changed since compilation (--selective)
       --changed-use: as newuse, but does not trigger reinstallation when flags that the user has
         not enabled are added or removed (--selective)
       --selective: (aka --noreplace) skips packages on the command-line that are already installed

    Mask message:
    # Mike Gilbert <floppym@gentoo.org> (13 Nov 2017)
    # python-updater is obsolete. Utilize PYTHON_TARGETS and
    # emerge --changed-use to rebuild packages instead.
    # Removal in 30 days.
    """
    ctx.emerge('--update --changed-use --keep-going {}'.format(target))

@task(aliases=['emerge'])
def merge(ctx, target='world'):
    """perform a changed use merge"""
    ctx.emerge('--update --changed-use --keep-going {}'.format(target))

