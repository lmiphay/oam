# -*- coding: utf-8 -*-

import os
import glob

from invoke import task

OAM_LOGDIR   = os.getenv('OAM_LOGDIR', '/var/log/oam')
OAM_KEEPLOGS = int(os.getenv('OAM_KEEPLOGS', '10'))

@task(default=True)
def expire(ctx):
    with ctx.cd(OAM_LOGDIR):
        for day in glob.glob('2*')[0:-OAM_KEEPLOGS]:
            shutil.rmtree(day)
