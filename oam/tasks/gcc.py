# -*- coding: utf-8 -*-

import os.path

from invoke import task

"""
1. generate list of packages (manifest) to build on the host
2. configure build settings in container to match the host
3. bring container up to date (check /usr/portage/packages is writable from container)
4. parse list and build a binary package of anything which is not already available as a binary package
5. finally install the packages on the host
"""

PKGDIR = os.getenv('PKGDIR', '/usr/portage/packages')
BUILD_OPT = '-1 --verbose --keep-going --buildpkg=y'
INSTALL_OPT = '-1 --usepkgonly=y --nodeps --verbose --binpkg-changed-deps=y --with-bdeps=n'

def pkg_exists(atom):
    return os.path.isfile('{}/{}.tbz2'.format(PKGDIR, atom))

def packages(manifest):
    """ convert:
           [ebuild   R    ] dev-libs/liborcus-0.11.2  PYTHON_SINGLE_TARGET="(-python3_6)" PYTHON_TARGETS="(-python3_6)" 
        to:
           dev-libs/liborcus-0.11.2
    """
    for line in open(manifest, 'r').readlines():
        if line.startswith('[ebuild'):
            yield re.sub(r'^\[[^]]+\] ([^: ]+).*', r'=\1', line.strip())

def unbuilt(manifest):
    """yields a list of packages which have not yet been built """
    for atom in packages(manifest):
        if not pkg_exists(atom):
            yield atom

@task
def build(ctx, manifest):
    """build packages in the container"""
    ctx.run('emerge {} {}'.format(BUILD_OPT, ' ='.join(unbuilt(manifest))), echo=True)

@task
def install(ctx, manifest):
    """install packages on the server"""
    ctx.run('emerge {} {}'.format(INSTALL_OPT, ' ='.join(packages(manifest))), echo=True)

@task
def manifest(ctx):
    """generate list of packages to rebuild
       see: new item from 2015-10-22: GCC 5 Defaults to the New C++11 ABI
    """
    ctx.run("revdep-rebuild --pretend --library 'libstdc++.so.6' -- --exclude gcc")
