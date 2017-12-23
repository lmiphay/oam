# -*- coding: utf-8 -*-
"""
Can use like this:
  1. oam task depclean
     which will produce a list like:

     =app-text/docbook-xml-dtd-4.4-r2
     =app-text/xmlto-0.0.26-r1
     =dev-lang/nasm-2.12.01
     =dev-libs/libnatspec-0.2.6-r1
     =dev-util/desktop-file-utils-0.23

   2. emerge --noreplace <whatever_want_to_add_to_world>
   3. emerge -aC $(oam task depclean)
   4. revdep-rebuild --ignore
"""
from __future__ import print_function
import os
import subprocess
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
    ctx.emerge('--update --newuse --deep --with-bdeps=y world', echo=True)

@task
def remove(ctx, opt='--pretend'):
    """run an 'emerge --depclean' (sets --pretend by default)"""
    return ctx.run('emerge {opt} --depclean'.format(opt=opt),
                   echo=True,
                   capture_buffer_size=10240).stdout

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
    print('### Packages which would be removed:')
    filtered = []
    for atom in reformat(remove(ctx)):
        if is_filtered(atom):
            filtered.append(atom)
        else:
            print(atom)
    print('### Filtered from above list: {}'.format(', '.join(filtered)))

@task
def rebuild(ctx):
    """Run a revdep rebuild to check system consistency"""
    ctx.run('revdep-rebuild --ignore', echo=True)

@task(pre=[newuse, removal_list], post=[call(remove, opt=''), rebuild])
def clean(ctx):
    """Run:
       1. an emerge newuse update
       2. list the packages which would be removed by a depclean
       3. wait for the RETURN key to confirm removal (control-C to abort)
       4. run an emerge depclean (note not currently filtered).
       5. run a revdep-rebuild
    """
    subprocess.call('read -p "Pressing RETURN will _REMOVE_ any packages listed above"', shell=True)

@task
def add(ctx, atom):
    """add package to the world file without rebuilding it"""
    ctx.emerge('--noreplace {}'.format(atom), echo=True)
