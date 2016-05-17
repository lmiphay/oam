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
from .direct import Direct, target_matches
import subprocess

class Runner(object):

    def __init__(self, target):
        self.logger = ServersLog('direct')
        self.target = target

    def provider(self):
        if direct.target_matches(self.target):
            return Direct()
        else:
            return None

@cli.command()
@click.option('--target', default='localhost',
              help='server to run command on')
@click.option('--log', default='direct',
              help='log output to this facility')
@click.argument('cmd')  # the command to run
def runner(target, log, cmd):
    """Run cmd on server using an appropriate backed provider
       Example:
       $ oam runner --target localhost --log build 'emerge --update world'
    """
    if len(cmd)<1:
        sys.exit("no command?")
    else:
        return Runner(target).provider().run(step = { 'cmd': cmd, 'log': log })
