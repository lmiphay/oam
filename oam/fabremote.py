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
import fabric

def is_lxc():
    """Return True if the server is an lxc, False otherwise"""
    return fabric.contrib.files.contains('/proc/1/cgroup', '/lxc/')

def is_docker():
    """Return True if the server is a docker, False otherwise"""
    return fabric.contrib.files.contains('/proc/1/cgroup', '/docker/')

@fabric.api.task
def fab_remote(cmd, logger):
    with fabric.api.settings(warn_only=True):
        result = fabric.api.run(cmd,
                                stdout=logger.out(env.host),
                                stderr=logger.err(env.host),
                                combine_stderr=False)
        if result.failed:
            logger.fail(env.host, result)
        return result

class FabRemote(object):

    def __init__(self, servers):
        self.servers = servers
        self.logger = ServersLog(servers)

    def drive(self, step):
        return execute(fab_remote,
                       step['cmd'],
                       self.logger.step(step['log']),
                       hosts=self.servers)
q
@cli.command()
@click.option('--log', default='fabremote', help='log all output using this facility')
@click.argument('servers')        # csv list of servers (no spaces)
@click.argument('cmd', nargs=-1)  # the command to run on the above servers
def fabremote(log, servers, cmd):
    """Run cmd on each of the specified servers"""
    step = {
        'cmd': ' '.join(cmd),
        'log': log
        }
    return Fabremote(servers.split(',')).drive(step)
