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
from .daylog import DAYLOG

class ServersLog(object):

    def __init__(self, servers):
        self.logger = logging.getLogger("oam.serverslog")
        self.servers = servers
        self.logname = None

    def hostdir(self, host):
        dirname = '/var/log/oam/{}/{}'.format(DAYLOG.current_day(), host)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        return dirname

    def set_logname(self, logname):
        self.logname = logname

    def out(self, host):
        return open('{}/{}.log'.format(self.hostdir(host), self.logname), 'a')

    def err(self, host):
        return open('{}/error.log'.format(self.hostdir(host)), 'a')

    def fail(self, host, result):
        self.logger.error('%s %s %s', host, str(result.result_code), result.stderr)
        return 1
