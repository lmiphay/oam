#!/usr/bin/python

from __future__ import print_function
import sys
import logging
import click

@click.group(invoke_without_command=True)
@click.option('--debug/--no-debug', default=False, envvar='OAM_DEBUG')
@click.pass_context
def cli(ctx, debug):
    if debug:
        loglevel = logging.DEBUG
    else:
        loglevel = logging.INFO

    logging.basicConfig(level=loglevel,
                        format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger("oam.main")
    logger.log(logging.DEBUG, 'sys.path=%s', str(sys.path))
    logger.log(logging.DEBUG, 'sys.argv=%s', str(sys.argv))

    if ctx.invoked_subcommand is None:
        logger.log(logging.DEBUG, 'no subcommand')
    else:
        logger.log(logging.DEBUG, 'subcommand: %s', ctx.invoked_subcommand)
