# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import subprocess
import pprint

import click
from .cmd import cli
from oam.daylog import last_day
from oam.status import Status
import oam.settings

STATUS_CMD = 'oam status --yaml-format --day='

class Review(object):

    def __init__(self, day, multicolumn, lxc, width, servers):
        self.day = day
        self.multicolumn = multicolumn
        self.lxc = lxc
        self.width = width
        if len(servers) == 0:
            self.servers = oam.settings.oam.review.hosts
        else:
            self.servers = servers

    def run(self):
        cmd = '{}{}'.format(STATUS_CMD, self.day)
        self.report = {}
        for host in self.servers:
            self.report[host] = [ 'server: {}'.format(host) ]
            if host == 'localhost':
                self.report[host].extend(Status(self.day, yaml_format=True).run().split('\n'))
            else:
                self.report[host].extend(subprocess.check_output('ssh {} {}'.format(host, cmd), shell=True).split('\n'))
        if self.multicolumn:
            return self.render_multicolumn()
        else:
            return [self.report[host] for host in self.servers]

    def render_multicolumn(self):
        i = 0
        result = []
        while True:
            multicol = ''
            finished = True
            for host in self.servers:
                if i<len(self.report[host]):
                    line = self.report[host][i].ljust(self.width, '.')[0:self.width]
                    finished = False
                else:
                    line = ','*self.width
                multicol = multicol + line + ' |'
            result.append(multicol)
            i += 1
            if finished:
                break
        return result

    def lxcs(self, host):
        return subprocess.check_output('ssh {} sudo lxc-ls --active'.format(host), shell=True).split()

@cli.command()
@click.option('--day', default=last_day(), help='day logs to process')
@click.option('--multicolumn', is_flag=True, help='write a multicolumn hosts report')
@click.option('--lxc', is_flag=True, help='include lxc\'s')
@click.option('--width', default=78, help='column width in multicolumn mode')
@click.argument('servers', nargs=-1, envvar='OAM_REVIEW_HOSTS')
def review(day, multicolumn, lxc, width, servers):
    """Generate status reports for each server"""
    pprint.pprint(Review(day, multicolumn, lxc, width, servers).run())
    return 0
