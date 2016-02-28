#!/usr/bin/python

from __future__ import print_function
import os
import subprocess
import click
from .cmd import cli

@cli.command(name='go')
def gocmd():
    """Kick off the configured default oam operation"""
    default_op = os.getenv('OAM_GO', 'oam-flow weekly')
    return subprocess.call('echo " { ' + default_op + ' ; } " | bash',
                           shell=True)
