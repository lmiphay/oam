# -*- coding: utf-8 -*-

from __future__ import print_function
import click
from .cmd import cli

__version__ = '5.0.0'

def get_version():
    return __version__

@cli.command()
def version():
    """Print oam version"""
    print(get_version())
