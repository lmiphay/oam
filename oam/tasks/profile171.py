# -*- coding: utf-8 -*-
#
"""
ref: 2017-12-26-experimental-amd64-17-1-profiles news article
https://www.gentoo.org/support/news-items/2017-12-26-experimental-amd64-17-1-profiles.html

  oam go
  emerge -1v app-portage/unsymlink-lib
  unsymlink-lib --analyze
  unsymlink-lib --migrate --pretend
  unsymlink-lib --migrate
  <reboot>
  emerge --info
  unsymlink-lib --finish --pretend
  unsymlink-lib --finish
  eselect profile set --force default/linux/amd64/17.1/desktop
  emerge -v1 sys-devel/gcc
  emerge -1v /lib32 /usr/lib32
  rm /lib32 /usr/lib32

Usage:

  # oam task profile171.phase1
  # reboot
  # oam task profile171.check
  # oam task profile171.phase2

"""
from __future__ import print_function

import glob
import yaml
from invoke import task
from invoke.tasks import call

CHOST = 'x86_64-pc-linux-gnu'

PROFILE171 = 'default/linux/amd64/17.1'
TARGET_PROFILE = '{}/desktop/plasma'.format(PROFILE171)

GCC_VER = '6.4.0'
GCC_ATOM = 'sys-devel/gcc:{}'.format(GCC_VER)

PHASE_1 = [
    'oam go',
    'emerge -1v app-portage/unsymlink-lib',
    'unsymlink-lib --analyze',
    'unsymlink-lib --migrate'
]
PHASE_2 = [
    'unsymlink-lib --finish',
    'eselect profile set --force {}'.format(TARGET_PROFILE),
    'emerge -v1 sys-devel/gcc',
]


@task
def phase(ctx, cmds):
  for cmd in cmds:
      ctx.run(cmd)

@task(pre=[call(phase, cmds=PHASE_1)])
def phase1(ctx):
    print('now reboot')

@task(pre=[call(phase, cmds=['emerge --info', 'unsymlink-lib --finish --pretend'])])
def check(ctx):
    pass

@task
def merge(ctx, atom):
    with ctx.prefix('. /etc/profile'):
        ctx.run('emerge -1 {}'.format(atom), echo=True, capture_buffer_size=200)

def is_installed(atom, major_version):
    """return True if the package is installed, -rX versions are counted"""
    return len(glob.glob('/var/db/pkg/{}-{}*'.format(atom, major_version))) > 0

@task
def gcc_config(ctx):
    """check that 6.4.0 is actually installed already"""
    if not is_installed('sys-devel/gcc', GCC_VER):
        merge(ctx, GCC_ATOM)
    ctx.run('gcc-config {}-{}'.format(CHOST, GCC_VER), echo=True)

@task(pre=[call(phase, cmds=PHASE_2), gcc_config, call(merge, GCC_ATOM), call(merge, '/lib32 /usr/lib32')])
def phase2(ctx):
    ctx.run('rm /lib32 /usr/lib32')

def current_profile(ctx):
    return ctx.run('eselect profile show | tail -1', echo=True).stdout.strip()

@task
def profile(ctx):
    if not current_profile(ctx).startswith(PROFILE17):
        ctx.run('eselect profile set {}'.format(DEFAULT_PROFILE), echo=True)

def profile_config(ctx):
    return {
        'profile': current_profile(ctx),
        'gcc': ctx.run('gcc-config -c').stdout.strip(),
        'binutils': ctx.run('eselect binutils show').stdout.strip()
    }

@task
def report(ctx):
    print(yaml.dump(profile_config(ctx), default_flow_style=False))

