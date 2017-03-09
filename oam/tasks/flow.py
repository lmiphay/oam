# -*- coding: utf-8 -*-

import os
import logging
import StringIO
import csv

import invoke
from invoke import task

FLOW = StringIO.StringIO(os.getenv('OAM_FLOW', ''))

# https://github.com/pyinvoke/invoke/issues/63
# threads = map(lambda x: Thread(target=x), (coffee, sass))
# [x.start() for x in threads]
# [x.join() for x in threads]

@task
def flow(ctx, stream=FLOW):
    for line in stream.readlines():
        for command in csv.reader([line], delimiter=' ', quotechar='"'):
            logging.info('run step %s', command)
            ctx.run(command)
            logging.info('step %s complete', command)

@task(flow)
def all(ctx):
    logging.info('flow done')
