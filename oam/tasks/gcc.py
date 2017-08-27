# -*- coding: utf-8 -*-

import os.path
import re

from invoke import task

"""
1. host: generate list of packages (manifest) to build on the host
2. container: configure to match the host
    a. /etc/portage/make.conf (CPPFLAGS/LDFLAGS, ACCEPT_LICENSE, VIDEO_CARDS, use flags...)
    b. /etc/portage/package.use
    c. /etc/portage/package.provided (e.g. may want to provide kernel sources (couldn't get that to work))
    d. /etc/portage/package.keywords for relevant packages
    d. depclean the container (optional)
3. container: bring up to date (inc newuse) (check /usr/portage/packages is writable from container)
4. container: build a binary package of anything which is not already available as a binary package (use manifest from step 1)
5. host: switch to gcc 5.x and install the binary packages (with extraopts='--pretend' first)
6  clean binary packages down

Notes:
   if qt conflicts, just remove from manifest and let portage decide which packages are actually needed
   drop eix if the eix cache is bind mounted ro into the container (it tries to write to it)
   maybe drop chromium, libreoffice from manifest and rebuild on host later
"""

PKGDIR = os.getenv('PKGDIR', '/usr/portage/packages')
BUILD_OPT = '-1 --verbose --verbose-conflicts --keep-going --buildpkg=y'
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
            yield re.sub(r'^\[[^]]+\] ([^: ]+).*', r'\1', line.strip())

def unbuilt(manifest):
    """yields a list of packages which have not yet been built"""
    for atom in packages(manifest):
        if not pkg_exists(atom):
            print 'Will-build: ', atom
            yield atom
        else:
            print 'Already-built: ', atom

@task
def manifest(ctx):
    """host: generate list of packages to rebuild
       see: new item from 2015-10-22: GCC 5 Defaults to the New C++11 ABI
    """
    ctx.run("revdep-rebuild --pretend --library 'libstdc++.so.6' -- --exclude gcc")

@task
def update(ctx):
    """container: update to match host use setting"""
    ctx.run('emerge --update --newuse --deep --verbose world',
            echo=True,
            capture_buffer_size=200)

@task
def build(ctx, manifest, extraopt=''):
    """container: build packages"""
    ctx.run('emerge {} {} ={}'.format(extraopt, BUILD_OPT, ' ='.join(unbuilt(manifest))),
            echo=True,
            capture_buffer_size=200)

@task
def install(ctx, manifest, extraopt=''):
    """host: install packages"""
    ctx.run('emerge {} {} ={}'.format(extraopt, INSTALL_OPT, ' ='.join(packages(manifest))),
            echo=True,
            capture_buffer_size=200)


