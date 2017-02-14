# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import logging
import click
from .cmd import cli

import invoke

@invoke.task
def sync(ctx):
    ctx.run('echo sync!')
    
@invoke.task
def summary(ctx):
    ctx.run('echo summary!')
    
@invoke.task(default=True, pre=[sync], post=[summary])
def update(ctx):
    ctx.run('echo update!')

@cli.command(name='invoke')
@click.argument('tasks', nargs=-1)
def oaminvoke(tasks):
    """Sequentially invoke one or more tasks"""
    logger = logging.getLogger("oam.invoke")
    
    ns = invoke.Collection()
    ns.add_task(update)
    ns.add_task(sync)
    ns.add_task(summary)
    
    executor = invoke.Executor(ns)
    
    for task in tasks:
        logger.log(logging.INFO, 'invoking %s', task)
        result = executor.execute((task, {}))
        logger.log(logging.INFO, '  result %s', str(result))
        
    return 0
