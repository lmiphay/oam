# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import invoke

from oam.logdest import logdest

class Context(invoke.Context):

    def __init__(self, config=None):
        super(Context, self).__init__(config)

    # new flags: if_installed, pretend
    def run(self, command, **kwargs):
        oamlog_write(command)
        print('in oaminvoke.Context run')
        kwargs['out_stream'], kwargs['err_stream'] = logdest(command)
        runner_class = self.config.get('runner', invoke.Local)
        return runner_class(context=self).run(command, **kwargs)

    # new flags: if_new_rev=atom
    def emerge(self, args, **kwargs):
        return self.run(cmd, kwargs)

    # flags: force
    def rebuild_preserved(self, args):
        if len(preserved_libs())>0:
            self.emerge(opts='--keep-going', target='@preserved-rebuild')
