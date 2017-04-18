# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import subprocess
import logging
import time
import click

from .cmd import cli
from .options import oam_config

@cli.command(name='go')
def gocmd():
    """Kick off the configured default oam operation"""
    default_op = oam_config('oam_go')
    return subprocess.call('echo " { ' + default_op + ' ; } " | bash',
                           shell=True)

FG_CMD = 'ssh {} "{}"'
BG_CMD = 'ssh {} "screen -dmS {} {}"'
SESSION_NAME = 'bg-oam'

@cli.command(name='bg')
@click.option('--wait/--no-wait', default=False, help="wait for operations to complete")
@click.option('--command', default='oam go', help="command to run")
@click.argument('targets', nargs=-1)
def bg(wait, command, targets):
    """Run the default oam operation on targets"""
    procs = []
    if len(targets)==0:
        targets = ['localhost']
    for server in targets:
        if wait:
            cmd = FG_CMD.format(server, command)
        else:
            cmd = BG_CMD.format(server, SESSION_NAME, command)
        logging.info('%s start, cmd: %s', server, cmd)
        procs.append(subprocess.Popen(cmd, shell=True))
    finished = 0
    while finished != len(procs):
        for index, server in enumerate(procs):
            logging.debug('looping at %s %d', targets[index], finished)
            if not server.poll() is None:
                finished += 1
        time.sleep(1)
    for index, server in enumerate(procs):
        server.wait()
        logging.info('%s finish, returncode=%d', targets[index], server.returncode)
