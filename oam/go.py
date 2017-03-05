# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import subprocess
import click

from .cmd import cli
from .options import oam_config

@cli.command(name='go')
def gocmd():
    """Kick off the configured default oam operation"""
    default_op = oam_config('oam_go')
    return subprocess.call('echo " { ' + default_op + ' ; } " | bash',
                           shell=True)
