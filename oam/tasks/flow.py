# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import StringIO
import csv
import threading

import invoke
from invoke import task

import oam.tasks

FLOW = StringIO.StringIO(os.getenv('OAM_FLOW', ''))

@task(help={'task': 'Name of the oam task to run'})
def step(ctx, task):
    """executes one single oam task"""
    oam.oaminvoke.Executor(oam.tasks.ns).execute((task, {}))

@task(help={'tasks': 'a string with a space delimited list of tasks to execute in parallel'})
def stage(ctx, tasks):
    """parallel execution of the tasks in a stage.
       see: https://github.com/pyinvoke/invoke/issues/63
    """
    threads = []
    for task in csv.reader([tasks], delimiter=' ', quotechar='"'):
        if command.startswith('oam-'):
            threads.append(threading.Thread(name=command, target=step, args=(ctx, command['oam-':])))
        else:
            threads.append(threading.Thread(name=command, target=ctx.run, args=(ctx, command)))
    [x.start() for x in threads]
    [x.join() for x in threads]

@task(default=True, help={'stream': 'the specific flow to execute, a multi-task stage per line'})
def flow(ctx, stream=FLOW):
    """sequential flow runner"""
    for line in stream.readlines():
        stage(ctx, line)

@task
def show(ctx):
    print(FLOW)
