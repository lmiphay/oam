# -*- coding: utf-8 -*-

from invoke import task

DEFAULT_OPTS = '--backtrack=50 --deep --verbose --verbose-conflicts'

@task
def emerge(ctx, default_opts=DEFAULT_OPTS, opts='', target='world', tag=''):
    ctx.run('ionice -c3 {} /usr/bin/emerge {} {} {}'.format(tag, default_opts, opts, target))
