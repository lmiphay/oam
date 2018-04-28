# -*- coding: utf-8 -*-

import logging

import invoke
from invoke import task

import oam.path
from oam.qcheck import QCheck
import oam.log
import oam.daylog
import oam.fact

@task(default=True)
def qcheck(ctx):
    """( oam qcheck > $(oam_logfile qcheck) ) 2> >(oam_err "qcheck")
       ctx.run('oam qcheck')
    """
    oam.log.info('qcheck')

    with open(oam.path.log_file('qcheck'), 'w') as f:
        for it in QCheck().its():
            f.write('{}\n'.format(it))

    diffs = oam.fact.qcheckdiff.fact()['qcheck_diff']

    with open(oam.path.log_file('qcheck-diffs'), 'w') as f:
        f.write('---------------------\n')
        if len(diffs)<1:
            f.write('No \n')
        f.write('Differences\n')
        f.write('---------------------\n')
        for diff_line in diffs:
            f.write('{}\n'.format(diff_line))

    return 0
