#!/usr/bin/python

from __future__ import print_function
import click
from .cmd import cli

__version__ = '5.0.0'

@cli.command()
def version():
    """Print gentoo-oam version"""
    print(__version__)
