# -*- coding: utf-8 -*-

from __future__ import print_function
import sys

from invoke import task


# filter these packages - only remove if not the active versions
FILTER={
    'sys-devel/binutils',
    'sys-devel/gcc',
    'sys-kernel/gentoo-sources'
}


@task
def newuse(ctx):
    """bring the system up-to-date prior to a depclean run"""
    ctx.emerge('--update --newuse --deep --with-bdeps=y world')

@task
def remove(ctx, opt='--pretend'):
    """run an 'emerge --depclean' (sets --pretend by default)"""
    return ctx.run('emerge {opt} --depclean'.format(opt=opt), capture_buffer_size=10240).stdout

def reformat(raw_output):
    """re-format the output of 'emerge --pretend --depclean world'"""
    for line in raw_output.splitlines():
        if 'All selected packages:' in line:
            for atom in sorted(line.replace('All selected packages:', '').split()):
                yield atom

def is_filtered(atom):
    for blacklist in FILTER:
        if blacklist in atom:
            return True
    return False

@task(default=True, aliases=['list'])
def removal_list(ctx):
    """list packages that would be removed"""
    for atom in reformat(remove(ctx)):
        if is_filtered(atom):
            print('X{}'.format(atom))
        else:
            print(atom)

@task
def add(ctx, atom):
    """add package to the world file without rebuilding it"""
    ctx.emerge('--noreplace {}'.format(atom))
