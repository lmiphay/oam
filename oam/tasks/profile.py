# -*- coding: utf-8 -*-

from __future__ import print_function

from invoke import task
from invoke.tasks import call


def current(ctx):
    """
    :return: the currently selected profile
    """
    return ctx.run('eselect profile show | tail -1', echo=True).stdout.strip()

@task
def select(ctx, newprofile):
    """
    Set a new profile (if it is not already in force)

    :param: newprofile is the target profile to select
    """
    if not current_profile(ctx).startswith(newprofile):
        ctx.run('eselect profile set {}'.format(newprofile), echo=True)

def facts(ctx):
    """
    :return: the currently selected profile, gcc and binutils
    """
    return {
        'profile': current_profile(ctx),
        'gcc': ctx.run('gcc-config -c').stdout.strip(),
        'binutils': ctx.run('eselect binutils show').stdout.strip()
    }

@task
def report(ctx):
    """
    Dump the current profile, gcc and binutils settings to stdout
    """
    print(yaml.dump(profile_config(ctx), default_flow_style=False))
