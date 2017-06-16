# -*- coding: utf-8 -*-

import os
import StringIO
import csv

from invoke import task

FLOW = StringIO.StringIO(os.getenv('OAM_FLOW', ''))

# https://github.com/pyinvoke/invoke/issues/63
# threads = map(lambda x: Thread(target=x), (coffee, sass))
# [x.start() for x in threads]
# [x.join() for x in threads]

@task(default=True)
def flow(ctx, stream=FLOW):
    for line in stream.readlines():
        for command in csv.reader([line], delimiter=' ', quotechar='"'):
            ctx.run(command, echo=True)
