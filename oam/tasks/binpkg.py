# -*- coding: utf-8 -*-

import re
from invoke import task

# see also: EMERGE_DEFAULT_OPTS in make.conf(5)

UPDATE  = '--update --deep --changed-use --changed-deps --backtrack=100'
QUIET   = '--quiet-build --quiet=y --color=n'
INSTALL = '--usepkg=y --keep-going'

@task
def pretend(ctx):
    ctx.pretend = ctx.run('emerge --pretend {} {} --columns --with-bdeps=n world'.format(UPDATE, QUIET)).stdout

@task(pretend)
def updates(ctx):
    """ 
[ebuild   R    ] virtual/editor                                        [0]                          
[ebuild   R    ] sys-process/audit                                     [2.6.4]                      
    """
    ctx.updates = [ re.findall(r'([-\w+]/[-\w+])', foo)[0] for line in ctx.pretend.splitlines() ]

@task(updates)
def build(ctx):
    for atom in ctx.updates:
        ctx.run('emerge --update --newuse --buildpkgonly {} {}'.format(QUIET, atom), echo=True)
    
@task(default=True, pre=[build])
def install(ctx):
    ctx.run('emerge {} {} --verbose --binpkg-changed-deps=y --with-bdeps=n world'.format(UPDATE, INSTALL), echo=True)
