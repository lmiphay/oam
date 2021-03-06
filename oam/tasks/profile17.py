# -*- coding: utf-8 -*-
#
"""
ref: 2017-11-30-new-17-profiles news article

From oam the usage should look like this:

  # oam task profile17
  gcc-config x86_64-pc-linux-gnu-6.4.0
  eselect binutils set x86_64-pc-linux-gnu-2.29.1
  . /etc/profile && emerge -1 sys-devel/libtool
  eselect profile show | tail -1
  eselect profile set default/linux/amd64/17.0/desktop/plasma
  . /etc/profile && emerge -1 sys-devel/gcc:6.4.0
  . /etc/profile && emerge -1 sys-devel/binutils
  . /etc/profile && emerge -1 sys-libs/glibc
  . /etc/profile && emerge -1 --exclude sys-libs/glibc /lib*/*.a /usr/lib*/*.a
  eselect profile show | tail -1
  binutils: !!python/unicode 'x86_64-pc-linux-gnu-2.29.1'
  gcc: !!python/unicode 'x86_64-pc-linux-gnu-6.4.0'
  profile: !!python/unicode 'default/linux/amd64/17.0/desktop/plasma'

  #
"""
from __future__ import print_function

import glob
import yaml
from invoke import task
from invoke.tasks import call

CHOST = 'x86_64-pc-linux-gnu'

PROFILE17 = 'default/linux/amd64/17.0'
DEFAULT_PROFILE = '{}/desktop/plasma'.format(PROFILE17)

GCC_VER = '6.4.0'
GCC_ATOM = 'sys-devel/gcc:{}'.format(GCC_VER)

BINUTILS_VER = '2.29.1-r1'
BINUTILS_ATOM = 'sys-devel/binutils'
BINUTILS_ESELECT = '{}-2.29.1'.format(CHOST)

def is_installed(atom, major_version):
    """return True if the package is installed, -rX versions are counted"""
    return len(glob.glob('/var/db/pkg/{}-{}*'.format(atom, major_version))) > 0

@task
def merge(ctx, atom):
    with ctx.prefix('. /etc/profile'):
        ctx.run('emerge -1 {}'.format(atom), echo=True, capture_buffer_size=200)

@task
def gcc_config(ctx):
    """check that 6.4.0 is actually installed already"""
    if not is_installed('sys-devel/gcc', GCC_VER):
        merge(ctx, GCC_ATOM)
    ctx.run('gcc-config {}-{}'.format(CHOST, GCC_VER), echo=True)

@task
def binutils(ctx):
    if not is_installed('sys-devel/binutils', BINUTILS_VER):
        merge(ctx, BINUTILS_ATOM)
    ctx.run('eselect binutils set {}'.format(BINUTILS_ESELECT), echo=True)

@task
def libtool(ctx):
    merge(ctx, 'sys-devel/libtool')

def current_profile(ctx):
    return ctx.run('eselect profile show | tail -1', echo=True).stdout.strip()

@task
def profile(ctx):
    if not current_profile(ctx).startswith(PROFILE17):
        ctx.run('eselect profile set {}'.format(DEFAULT_PROFILE), echo=True)

@task
def base(ctx):
    for atom in [GCC_ATOM, BINUTILS_ATOM, 'sys-libs/glibc']:
        merge(ctx, atom)

@task
def world(ctx):
    merge(ctx, '--keep-going -e @world')

@task
def minimum(ctx):
    """see: https://forums.gentoo.org/viewtopic-p-8149548.html#8149548
       also maybe: emerge -1 $(eix-installed-after -btF /usr/bin/gcc)
    """
    merge(ctx, '--exclude sys-libs/glibc /lib*/*.a /usr/lib*/*.a')

def profile_config(ctx):
    return {
        'profile': current_profile(ctx),
        'gcc': ctx.run('gcc-config -c').stdout.strip(),
        'binutils': ctx.run('eselect binutils show').stdout.strip()
    }

@task
def report(ctx):
    print(yaml.dump(profile_config(ctx), default_flow_style=False))

@task(default=True, pre=[gcc_config, binutils, libtool, profile, base], post=[minimum, report])
def update(ctx):
    pass
