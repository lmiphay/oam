#!/usr/bin/python

from __future__ import print_function
import sys
import os
import logging
import click
import subprocess
import re
import datetime
from .cmd import cli
from .serverslog import ServersLog
import subprocess

def is_lxc():
    """Return True if the server is an lxc, False otherwise"""
    return '/lxc/' in open('/proc/1/cgroup').read()
    
def is_docker():
    """Return True if the server is a docker, False otherwise"""
    return '/docker/' in open('/proc/1/cgroup').read()

class Direct(object):

    def __init__(self):
        self.logger = ServersLog('direct')

    def drive(self, step):
        self.logger.set_logname(step['log'])
        proc = subprocess.Popen(step['cmd'].split(' '),
                                bufsize=1, # line buffered
                                stdout=self.logger.out(),
                                stderr=self.logger.err())
        proc.wait()
        return proc.returncode

@cli.command()
@click.option('--log', default='direct',
              help='log all output using this facility')
@click.argument('cmd', nargs=-1)  # the command to run
def direct(log, cmd):
    """Run cmd on each of the local server"""
    step = {
        'cmd': ' '.join(cmd),
        'log': log
        }
    if len(step['cmd'])<1:
        sys.exit("no command?")
    else:
        return Direct().drive(step)
