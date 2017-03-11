# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import logging
import pprint
import click
from .cmd import cli

import invoke
import oam.tasks

@cli.command(name='invoke')
@click.option('--l', '-l', is_flag=True, default=None, help='list availble tasks')
@click.argument('tasks', nargs=-1)
def xoaminvoke(l, tasks):
    """Sequentially invoke one or more tasks"""
    logger = logging.getLogger("oam.invoke")

    if not l is None:
        pprint.pprint(oam.tasks.ns.task_names)
        return 0
    
    executor = invoke.Executor(oam.tasks.ns)
    
    for task in tasks:
        logger.log(logging.INFO, 'invoking %s', task)
        result = executor.execute((task, {}))
        logger.log(logging.INFO, '  result %s', str(result))
        
    return 0
