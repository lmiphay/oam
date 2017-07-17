# -*- coding: utf-8 -*-

import logging

import invoke
from invoke import task
import oam.path
from oam.qcheck import QCheck
import oam.log

@task(default=True)
def qcheck(ctx):
    """( oam qcheck > $(oam_logfile qcheck) ) 2> >(oam_err "qcheck")
       ctx.run('oam qcheck')
    """
    oam.log.info('qcheck')

    with open(oam.path.log_file('qcheck'), 'w') as f:
        for it in QCheck().its():
            f.write('{}\n'.format(it))
    return 0
