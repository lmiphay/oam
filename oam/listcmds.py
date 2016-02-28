#!/usr/bin/python

from __future__ import print_function
import sys
import os
import logging
import click
from .cmd import cli

@cli.command(name='list-cmds')
@click.pass_context
def listcmds(ctx):
    """List avaiable sub commands"""
    print(*cli.list_commands(ctx))
    return 0
