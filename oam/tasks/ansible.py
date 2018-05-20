# -*- coding: utf-8 -*-
"""
"""

from __future__ import print_function
import glob
from invoke import task, call
import oam.settings


ANSIBLE = 'ansible all --inventory "{hosts}," --module-name shell --args "{args} --forks {forks}"'


@task(iterable=['hosts'], default=True)
def ansible(ctx, hosts, inventory=None, args='oam go', forks=5):
    """Run the command(s) specified by args on the servers listed by the specified inventory key"""
    if not inventory is None:
        hosts.append(oam.settings.inventory[inventory])
    ctx.run(ANSIBLE.format(hosts=hosts, args=args, forks=forks))

@task(pre=[call(ansible, inventory='containers', forks=1)])
def containers(ctx):
    """Run 'oam go' on the containers specified by the 'container' inventory key"""
    pass

@task(pre=[call(ansible, inventory='dependant-servers')])
def servers(ctx):
    """Run 'oam go' on the servers specified by the 'dependent-servers' inventory key"""
    pass

@task(pre=[call(containers), call(servers)])
def both(ctx):
    """Run 'oam go' on the containers and servers specified by the
       'containers' and 'dependent-servers' inventory keys
    """
    pass

@task(name='resume-both', pre=[call(ansible, inventory='containers', args='oam resume', forks=1), call(ansible, inventory='dependant-servers', args='oam resume')])
def resume_both(ctx):
    """Run 'oam resume' on the containers and servers specified by the
       'containers' and 'dependent-servers' inventory keys
    """
    pass
