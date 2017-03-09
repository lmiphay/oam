# -*- coding: utf-8 -*-

import logging

from invoke import task, call

@task
def expire(ctx, oamdir='/var/log/oam', keeplogs=10, debug=''): # or: debug='echo'
    ctx.run("cd {} && ls -d1tr 2* | head -n -{} | xargs --verbose -d '\n' {} rm -rf".format(oamdir,
                                                                                            keeplogs,
                                                                                            debug))
@task(call(expire, debug='echo'))
def dryrun(ctx):
    logging.info('dryrun done')

@task(default=True, pre=[expire])
def all(ctx):
    logging.info('expiry done')
