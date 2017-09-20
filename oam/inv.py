# -*- coding: utf-8 -*-

import glob
import imp
import pprint
import os.path
import sys

import click

from oam.cmd import cli
import oam.log
import oam.tasks
import oam.oaminvoke
import oam.settings

import invoke
from invoke.tasks import Call # for monkey patch

def add_modules(ns, location):
    package = os.path.basename(os.path.dirname(location))

    oam.log.info('add modules from {} to invoke collection: {}'.format(location, package))

    try:
        sys.path.insert(0, location)

        for mod in glob.glob('{}/*.py'.format(location)):
            oam.log.info('  checking: {}'.format(mod))

            if not mod.endswith('__init__.py'):
                # foo = imp.load_source('module.name', '/path/to/file.py')
                modname = os.path.basename(mod)[:-3]
                oam.log.info('  load_source: {}.{} {}'.format(package, modname, mod))
                newmod = imp.load_source('{}.{}'.format(package, modname), mod)
                ns.add_collection(newmod)
    finally:
        del sys.path[0]

def oam_make_context(self, config):
    """
    Generate an oam Context for the call, using the given config.
    """
    return oam.oaminvoke.Context(config=config)

class Inv(object):

    def __init__(self):
        self.wire()
        add_modules(oam.tasks.ns, '/etc/oam/localtasks') # Fixme - need to run from source tree
        self.program = invoke.Program(namespace=oam.tasks.ns, version='0.0.1')

    def wire(self):
        """
        Hook-up oam runtime with the invoke library
        """
        Call.make_context = oam_make_context

    def run_parameterised_task(self, taskspec):
        argv = ['oaminv', taskspec['task_name']]
        for key, value in taskspec.iteritems():
            if key!='task_name':
                argv.append('--{}={}'.format(key, value))
        oam.log.info('task start - {}'.format(argv[1]))
        self.program.run(argv=argv)
        oam.log.info('task complete - {}'.format(argv[1]))

    def run_task(self, taskname):
        if type(taskname)==tuple:
            taskname = taskname[0]
        self.run_parameterised_task({'task_name': taskname})

    def run_tasks(self, steps):
        for step in steps:
            self.run_task(step)
        return 0

    def get_flow(self, flowname):
        if flowname in oam.settings.flows:
            return oam.settings.flows[flowname]
        else:
            oam.log.error('flow {} not found'.format(flowname))
            raise ValueError('flow {} not found'.format(flowname))

    def run_flow(self, flow):
        for step in flow:
            if type(step)==str:
                if step.startswith('+'):
                    self.run_flow(self.get_flow(step[1:]))
                else:
                    self.run_task(step)
            elif type(step)==dict:
                self.run_parameterised_task(self.get_flow(step))
            else:
                oam.log.info('phase - {}'.format(step))
                self.run_flow(step)

    def run_flows(self, flownames):
        for flowname in flownames:
            oam.log.info('flow start - {}'.format(flowname))
            self.run_flow(self.get_flow(flowname))
            oam.log.info('flow complete - {}'.format(flowname))

@cli.command()
@click.option('--l', '-l', is_flag=True, default=None, help='list available tasks')
@click.option('--flow', is_flag=True, default=True, help='arguments are flows (not tasks)')
@click.option('--task', is_flag=True, default=False, help='arguments are tasks (not flows)')
@click.argument('tasks', nargs=-1)
def inv(l, flow, task, tasks):
    """
    Sequentially invoke one or more tasks, or flows
    """

    if type(tasks)==str:
        tasks = [tasks]

    if l is not None:
        pprint.pprint(oam.tasks.ns.task_names)
        return 0
    elif task:
        return Inv().run_tasks(tasks)
    elif flow:
        return Inv().run_flows(tasks)
    else:
        oam.log.error('unclear if flow or step?')
        return 1

@cli.command()
@click.argument('flows', nargs=-1)
def flow(flows):
    """
    Sequentially invoke one (or more) flow(s)
    """
    return Inv().run_flows(flows)

@cli.command()
@click.argument('tasks', nargs=-1)
def task(tasks):
    """
    Sequentially invoke one (or more) tasks(s)
    """
    return Inv().run_tasks(tasks)
