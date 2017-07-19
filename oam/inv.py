# -*- coding: utf-8 -*-

import pprint

import click

from .cmd import cli

import oam.log
import oam.tasks
import oam.oaminvoke
import oam.settings

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

def run_flow(program, flow):
    for step in flow:
        if type(step)==str:
            oam.log.info('step - {}'.format(step))
            program.run(argv=['oaminvflow'] + [step])
        else:
            oam.log.info('phase - {}'.format(step))
            run_flow(program, step)

def run_flows(program, flownames):
    for flowname in flownames:
        flow = oam.settings.get_flow(flowname)
        if flow is not None:
            run_flow(program, flow)
        else:
            raise ValueError('flow {} not found'.format(flowname))

@cli.command()
@click.option('--l', '-l', is_flag=True, default=None, help='list available tasks')
@click.option('--vanilla', is_flag=True, default=False, help='run vanilla invoke')
@click.option('--flow', is_flag=True, default=True, help='arguments are flows (not steps)')
@click.option('--step', is_flag=True, default=False, help='arguments are steps (not flows)')
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

    if step:
        # tasks is a tuple so convert to a list and prepend a dummy program name entry
        program.run(argv=['oaminvoke'] + list(tasks))
    elif flow:
        run_flows(program, tasks)
    else:
        oam.log.error('unclear if flow or step?')

    # program.run will have called sys.exit(1) (or so) if there was an error

    return 0
