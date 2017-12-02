# -*- coding: utf-8 -*-
#
# ref: 2017-11-30-new-17-profiles
#
from __future__ import print_function
import os
from invoke import task
from invoke.tasks import call

PROFILE = 'default/linux/amd64/17.0/desktop/plasma'
GCC_VER = '6.4.0'
GCC_ATOM = 'sys-devel/gcc:{}'.format(GCC_VER)

@task
def merge(ctx, atom):
    with ctx.prefix('. /etc/profile'):
        ctx.run('emerge -1 {}'.format(atom), echo=True, capture_buffer_size=200)

@task
def gcc_config(ctx):
    """check that 6.4.0 is actually installed already"""
    if not os.path.isdir('/var/db/pkg/sys-devel/gcc-{}'.format(GCC_VER)): # -rX should be allowed as well
        merge(ctx, GCC_ATOM)
    ctx.run('gcc-config x86_64-pc-linux-gnu-{}'.format(GCC_VER), echo=True)

@task
def libtool(ctx):
    merge(ctx, 'sys-devel/libtool')

@task
def profile(ctx):
    ctx.run('eselect profile set {}'.format(PROFILE))

@task
def base(ctx):
    for atom in [GCC_ATOM, 'sys-devel/binutils', 'sys-libs/glibc']:
        merge(ctx, atom) # need to select latest binutils

@task
def world(ctx):
    merge('-e @world')

@task(default=True, pre=[gcc_config, libtool, profile, base], post=[world])
def update(ctx):
    pass
