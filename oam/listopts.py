#!/usr/bin/python

from __future__ import print_function
import click
from .cmd import cli

@cli.command(name='list-opts')
def listopts():
    """ There doesn't appear to be a way to query options from click?"""
    print('--help --debug')
