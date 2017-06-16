# -*- coding: utf-8 -*-

import logging
import pprint
import click
from .cmd import cli

import oam.tasks
import oam.oaminvoke

@cli.command()
@click.option('--l', '-l', is_flag=True, default=None, help='list availble tasks')
@click.argument('tasks', nargs=-1)
def inv(l, tasks):
    """Sequentially invoke one or more tasks"""
    logger = logging.getLogger("oam.invoke")

    if not l is None:
        pprint.pprint(oam.tasks.ns.task_names)
        return 0
    
    executor = oam.oaminvoke.Executor(oam.tasks.ns)
    
    for task in tasks:
        logger.log(logging.INFO, 'invoking %s', task)
        result = executor.execute((task, {}))
        logger.log(logging.INFO, '  result %s', str(result))
        
    return 0
