# -*- coding: utf-8 -*-

from __future__ import print_function
import subprocess

import click

from oam.cmd import cli
import oam.log
import oam.settings

@cli.group(invoke_without_command=True)
@click.pass_context
def helper(ctx):
    """List available helper routines"""
    if ctx.invoked_subcommand is None:
        print('Available helpers:')
        for command in ['edit', 'mtab', 'term']:
            print(command, oam.settings.helper[command])
            
def run(cmd, arg):
    """Run the specified program via subprocess"""
    oam.log.info('subprocess - {} {}'.format(cmd, arg))
    return subprocess.call('{} {}'.format(cmd, arg), shell=True)
    
@helper.command()
@click.argument('filename')
def edit(filename):
    """Call the configured editor"""
    return run(oam.settings.helper.editor, filename)
            
@helper.command()
@click.argument('filenames', nargs=-1)
def mtab(filenames):
    """Call the configured multi-tab editor"""
    return run(oam.settings.helper.multitab, ' '.join(filenames))

@helper.command()
@click.argument('program')
def term(program):
    """Run program in the configured terminal"""
    return run(oam.settings.helper.terminal, program)

