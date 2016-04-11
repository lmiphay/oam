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
    """Name/open normal-log and error-log files"""

    LOGROOT = os.getenv('OAM_LOGDIR', '/var/log/oam')
    HOSTNAME = os.uname()[1]

    def __init__(self, default_logname = 'unknown'):
        self.logger = logging.getLogger("oam.serverslog")
        self.daydir = '{}/{}'.format(self.LOGROOT, DAYLOG.current_day())
        self.logname = default_logname

    def hostdir(self, host):
        if host == None:
            host = self.HOSTNAME
        dirname = '{}/{}'.format(self.daydir, host)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)
        return dirname

    def set_logname(self, logname):
        self.logname = logname

    def out(self, host):
        return open('{}/{}.log'.format(self.hostdir(host), self.logname), 'a')

    def err(self, host):
        return open('{}/error-{}.log'.format(self.hostdir(host), self.logname), 'a')

    def fail(self, host, result):
        self.logger.error('%s %s %s', host, str(result.result_code), result.stderr)
        return 1
