#!/usr/bin/python

from __future__ import print_function
import sys
import os
import logging
import click
from .cmd import cli

@cli.command()
def dumpenv(level = logging.INFO):
    """Show the OAM configuration settings"""
    logger = logging.getLogger("oam.dumpenv")
    for key in sorted(os.environ):
        if key.startswith('OAM_'):
            logger.log(level, '%s=%s', key, os.getenv(key))
