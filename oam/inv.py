# -*- coding: utf-8 -*-

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

def run_flow(flow):
    for step in flow:
        if type(step)==str:
            program.run(argv=['oaminvflow'] + list(step))
        else:
            run_flow(step)

def run_flows(flownames):
    for flowname in flownames:
        flow = settings.get_flow(flowname)
        if flow is not None:
            run_flow(flow)
        else:
            raise ValueError('flow {} not found'.format(flowname))

@cli.command()
@click.option('--l', '-l', is_flag=True, default=None, help='list available tasks')
@click.option('--vanilla', is_flag=True, default=False, help='run vanilla invoke')
@click.option('--flow', is_flag=True, default=False, help='arguments are flows (not steps)')
@click.argument('tasks', nargs=-1)
def inv(l, vanilla, tasks, flow):
    """
    Sequentially invoke one or more tasks, or flows
    """

    if l is not None:
        pprint.pprint(oam.tasks.ns.task_names)
        return 0
    
    program = invoke.Program(namespace=oam.tasks.ns, version='0.0.1')

    if not vanilla:
        oam_wire()

    if flow:
        run_flows(tasks)
    else:
        # tasks is a tuple so convert to a list and prepend a dummy program name entry
        program.run(argv=['oaminvoke'] + list(tasks))

    # program.run will have called sys.exit(1) (or so) if there was an error

    return 0
