# -*- coding: utf-8 -*-
#
# ref: 2017-11-30-new-17-profiles
#
from __future__ import print_function
from invoke import task

@task
def gcc(ctx):
    ctx.run('gcc-config x86_64-pc-linux-gnu-6.4.0', echo=True)

@task
def libtool(ctx):
    with ctx.prefix('. /etc/profile'):
        ctx.run('emerge -1 sys-devel/libtool', echo=True, capture_buffer_size=200)

@task
def profile(ctx):
    ctx.run('eselect profile set default/linux/amd64/17.0/desktop/plasma')

@task
def base(ctx):
    with ctx.prefix('. /etc/profile'):
        ctx.run('emerge -1 sys-devel/gcc:6.4.0', echo=True, capture_buffer_size=200)
        ctx.run('emerge -1 sys-devel/binutils', echo=True, capture_buffer_size=200)
        ctx.run('emerge -1 sys-libs/glibc', echo=True, capture_buffer_size=200)

@task
def world(ctx):
    with ctx.prefix('. /etc/profile'):
        ctx.run('emerge -e @world', echo=True, capture_buffer_size=200)

@task(pre=[gcc, libtool, profile, base, world])
def update(ctx):
    pass
