#!/usr/bin/python

from __future__ import print_function
import sys
import os
import logging
import click
import subprocess
import re
import datetime
import time
from .cmd import cli

"""
Recipe to create a gentoo lxc (gentoo running inside an lxc container)

The lxc-create command can be broken down into two parts:
   1. generic lxc-create options
   2. options which are specific to the gentoo template
"""
class LxcCreate(object):
    
    CACHEDIR = '/var/cache/lxc/gentoo'  # template scratch area
    
    CMD = (
        'lxc-create '
        '--template={template} '
        '--name={name} '
        '--lxcpath={lxcpath} '         # or -P, current=`lxc-config lxc.lxcpath`, default='/var/lib/lxc'
        '--dir={rootfs} '              # Place rootfs directory under DIR
        '--logfile={logfile} '
        '--logpriority={logpriority} '
        '-- '                          # gentoo template specific options from here on
        '--portage-dir={portagedir} ',
    )

    DEFAULT_CONFIG = {
        # lxc-create settings
        'template': 'gentoo',
        # 'name': None,
        'lxcpath': '/etc/lxc',
        'rootfs': '/lxc',
        'logfile': '/var/log/lxc-create.log',
        'logpriority': 'DEBUG',
        'portagedir': '/usr/portage',
    }
    
    # optional gentoo template specific parameters - create works without any of these being set
    POSTOPT = {
        'stage3': '--tarball={} ',             # e.g. /lxc/stage3-amd64-20160218.tar.bz2 '
        'mirror': '--mirror={} '               # e.g. http://distfiles.gentoo.org (<gentoomirror>)
        'flushcache': '--flush-cache ',
        'privateportage': '--private-portage', # don't mount portage from host (also -P)
    }

    # ROOTFS_PATH = '--rootfs=/lxc' # duplicates generic --dir option...

    def __init__(self, name, **kwargs):
        self.logger = logging.getLogger("oam.createlxc")
        self.config = dict({'name': name }, **self.DEFAULT_CONFIG)
        self.opts = kwargs
        self.portage_tarball = '{}/portage.tbz'.format(self.CACHEDIR)
        
    def prepare(self):
        """Manipulate the template cache as requested"""
        if not os.path.isdir(self.CACHEDIR):
            os.makedirs(self.CACHEDIR)
        if self.opts['privateportage']:
            if os.stat(self.portage_tarball).st_size == 0:
                os.remove(self.portage_tarball)
        else:
            if not os.path.isfile(self.portage_tarball):
                open(self.portage_tarball, 'w')          # dont download the portage snapshot

    """Create a new lxc container"""
    def create(name, tarball=None, mirror=None):
        cmd = self.CMD[0].format(**self.config)
        
        if self.opts['stage3']:
            cmd += self.POSTOPT['stage3'].format(self.opts['stage3'])
        if self.opts['privateportage']:
            cmd += self.POSTOPT['privateportage']
        if self.opts['mirror']:
            cmd += self.POSTOPT['mirror'].format(self.opts['mirror'])
        if self.opts['flushcache']:
            cmd += self.POSTOPT['flushcache']
                
        print(cmd)
        
        return subprocess.call(cmd)

@cli.command()
@click.option('--stage3', default=None, envvar='OAM_STAGE3', help='stage3 tarball location')
@click.option('--privateportage/--no-privateportage', default=False, help="don't mount /usr/portage from the host"):
@click.option('--flushcache/--no-flushcache', default=False, help='remove the gentoo template cache before lxc creation')
@click.option('--mirror', default=None, help='gentoo mirror site (e.g. http://distfiles.gentoo.org)')
@click.argument('name', help='name of the lxc to create')
@click.pass_context
def createlxc(ctx, stage3, privateportage, flushcache, mirror, name):
    """Create a new gentoo lxc container"""
    opts = {
        'stage3': stage3,
        'privateportage': privateportage,
        'flushcache': flushcache,
        'mirror': mirror
    }
    return LxcCreate(name, **opts).create()
