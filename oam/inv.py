# -*- coding: utf-8 -*-

import logging
import pprint
import click
from .cmd import cli

import oam.tasks
import oam.oaminvoke

import invoke
from invoke.tasks import Call

def oam_make_context(self, config):
    """
    Generate an oam Context for the call, using the given config.
    """
    return oam.oaminvoke.Context(config=config)

def oam_wire():
    """
    Hook-up oam runtime with the invoke library
    """
    Call.make_context = oam_make_context

@cli.command()
@click.option('--l', '-l', is_flag=True, default=None, help='list availble tasks')
@click.option('--vanilla', is_flag=True, default=False, help='run vanilla invoke')
@click.argument('tasks', nargs=-1)
def inv(l, vanilla, tasks):
    """
    Sequentially invoke one or more tasks
    """
    logger = logging.getLogger("oam.invoke")

    if not l is None:
        pprint.pprint(oam.tasks.ns.task_names)
        return 0
    
    program = invoke.Program(namespace=oam.tasks.ns, version='0.0.1')

    if not vanilla:
        oam_wire()

    program.run(tasks)

    return 0