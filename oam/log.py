# -*- coding: utf-8 -*-

import sys
import os
import logging
import click
import subprocess
import re
import datetime
from .cmd import cli

import oam.path

"""
Usage:
      self.logger = oam.logging.getLogger(__name__)
"""

OAM_LOGGER = None

def getLogger(ident=''):
    global OAM_LOGGER

    if OAM_LOGGER is None:
        logging.getLogger('').handlers = []
        logging.basicConfig(filename=oam.path.log_file(),
                            format='%(asctime)s %(levelname)s %(name)s - %(message)s',
                            datefmt='%Y%m%d:%H:%M:%S',
                            level=logging.INFO)
        OAM_LOGGER = logging.getLogger()

    if ident == '':
        return OAM_LOGGER
    else:
        return logging.getLogger(ident)

def critical(msg, *args, **kwargs):
    getLogger().critical(msg, *args, **kwargs)

def error(msg, *args, **kwargs):
    getLogger().error(msg, *args, **kwargs)

def debug(msg, *args, **kwargs):
    getLogger().debug(msg, *args, **kwargs)

def info(msg, *args, **kwargs):
    getLogger().info(msg, *args, **kwargs)

def warning(msg, *args, **kwargs):
    getLogger().warning(msg, *args, **kwargs)

def setLevel(lvl):
    getLogger().setLevel(lvl)

@cli.command()
@click.argument('msgs', nargs=-1)
def log(msgs):
    """log msgs to the default oam.log"""
    info(' '.join(msgs))
    logging.info('foo')
    return 0

