# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import subprocess
import logging
import time
import click
import eliot
import eliottree
import codecs

from .cmd import cli
from .options import oam_config

@cli.command(name='go')
def gocmd():
    """Kick off the configured default oam operation"""
    default_op = oam_config('oam_go')
    return subprocess.call('echo " { ' + default_op + ' ; } " | bash',
                           shell=True)

def render_stdout(message):
    """Ref:
       http://stackoverflow.com/questions/42936027/how-to-generate-eliot-tasks-for-eliottree-render-tasks
    """
    eliottree.render_tasks(codecs.getwriter('utf-8')(sys.stdout).write,
                           eliottree.tasks_from_iterable([message]),
                           colorize=True,
                           human_readable=True)

FG_CMD = 'ssh {} "{}"'
BG_CMD = 'ssh {} "screen -dmS {} {}"'
SESSION_NAME = 'bg-oam'

@cli.command(name='bg')
@click.option('--wait/--no-wait', default=False, help="wait for operations to complete")
@click.option('--command', default='oam go', help="command to run")
@click.option('--raweliot', default=True, help='Output raw eliot logs')
@click.argument('targets', nargs=-1)
def bg(wait, command, raweliot, targets):
    """Run the default oam operation on targets"""
    if raweliot:
        eliot.to_file(sys.stdout)
    else:
        # eliottree.render_tasks(sys.stdout.write, tasks, colorize=True) #py3
        eliot.add_destination(render_stdout)
    procs = []
    if len(targets)==0:
        targets = ['localhost']
    with eliot.start_task(action_type='run_ops', targets=targets):
        with eliot.start_action(action_type='start_ops', targets=targets):
            for server in targets:
                if wait:
                    cmd = FG_CMD.format(server, command)
                else:
                    cmd = BG_CMD.format(server, SESSION_NAME, command)
                logging.debug('%s start, cmd: %s', server, cmd)
                with eliot.start_action(action_type='start_process', target=server, cmd=cmd):
                    procs.append(subprocess.Popen(cmd, shell=True))
        finished = 0
        with eliot.start_action(action_type='wait_finishes', targets=targets):
            while finished != len(procs):
                for index, server in enumerate(procs):
                    logging.debug('looping at %s %d', targets[index], finished)
                    if not server.poll() is None:
                        eliot.Message.log(message_type='finish', target=targets[index])
                        finished += 1
                time.sleep(1)
        with eliot.start_action(action_type='wait_terminations', targets=targets):
            for index, server in enumerate(procs):
                with eliot.start_action(action_type='wait_process', target=targets[index]):
                    server.wait()
                    logging.debug('%s finish, returncode=%d', targets[index], server.returncode)
