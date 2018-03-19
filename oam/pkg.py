# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import os
import subprocess
import logging
import glob
import collections
import pprint
import click
from .cmd import cli
import portage
import oam.settings

class Pkg(object):

    ROOT = oam.settings.portage.configroot + '/var/db/pkg/'

    def __init__(self):
        pass

    def package(self, path):
        return os.path.relpath(path, self.ROOT)
                          
    def sizes(self):
        rec = collections.defaultdict(list)
        for filename in glob.iglob(self.ROOT + '*/*/SIZE'):
            size = int(open(filename).readline().strip())
            rec[size].append(self.package(os.path.dirname(filename)))
        for size, pkgs in sorted(rec.items()):
            for p in pkgs:
                print("%10d %s" % (size, p))

    def best_available(self, atom):
        return str(portage.db['/']['porttree'].dbapi.xmatch("bestmatch-visible", atom))

    def current_version(self, atom):
        return str(portage.best(portage.db['/']['vartree'].dbapi.match(atom)))

    def is_update_available(self, atom):
        return self.best_available(atom) != self.current_version(atom)

    def preserved_libs(self):
        return portage.db['/']["vartree"].dbapi._plib_registry.getPreservedLibs()

@cli.command()
def pkgsizes():
    """List installed packages ordered by size"""
    Pkg().sizes()

@cli.command()
def preservedlibs():
    """Return a list of preserved libraries (if any)"""
    print(pprint.pformat(Pkg().preserved_libs()))
    return 0

@cli.command()
@click.argument('atoms', nargs=-1)
def bestavailable(atoms):
    """List the best available versions in portage for the specified packages"""
    p = Pkg()
    for atom in atoms:
        print(p.best_available(atom))
    return 0

@cli.command()
@click.argument('atoms', nargs=-1)
def currentversion(atoms):
    """List the installed versions for the specified packages"""
    p = Pkg()
    for atom in atoms:
        print(pprint.pformat(p.current_version(atom)))
    return 0

@cli.command()
@click.argument('atom')
def updateavailable(atom):
    """Print Yes/No is there is an update available for the specified package"""
    avail = Pkg().is_update_available(atom)
    if avail:
        print('Yes')
    else:
        print('No')
    return 0


