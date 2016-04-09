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

class ServersLog(object):

    def __init__(self, servers):
        self.logger = logging.getLogger("oam.serverslog")
        self.servers = servers
        self.logid = None

    def set_step_id(self, logid):
        self.logid = logid

    def out(self, host):
        return open('/var/log/oam/{}/{}.log'.format(today(), self.logid), 'a')

    def err(self, host):
        return open('/var/log/oam/{}/error.log'.format(today()), 'a')

    def fail(self, result):
        self.logger.error(result.stderr)
        self.logger.error(result.result_code)
