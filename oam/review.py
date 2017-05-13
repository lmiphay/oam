# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import subprocess
import click
from .cmd import cli
from oam.daylog import last_day
from oam.status import Status

class Review(object):

    def __init__(self, day, servers):
        self.day = day
        if len(servers) == 0:
            self.servers = os.getenv('OAM_REVIEW_HOSTS', 'localhost').split()
        else:
            self.servers = servers

    def run(self):
        for host in self.servers:
            if host == 'localhost':
                print(Status(day).run())
            else:
                subprocess.call('ssh {} oam status --day={}'.format(host, self.day), shell=True)

@cli.command()
@click.option('--day', default=last_day(), help='day logs to process')
@click.argument('servers', nargs=-1)
def review(day, servers):
    """Generate status reports for each server"""
    Review(day, servers).run()
    return 0
