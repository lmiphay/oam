# -*- coding: utf-8 -*-

from __future__ import print_function

import invoke

class Context(invoke.Context):

    def __init__(self, config=None):
        super(OamContext, self).__init__(config)

    def run(self, command, **kwargs):
        print('in OamContext run')
        kwargs['out_stream'] = open('foobar.log', 'a')
        runner_class = self.config.get('runner', invoke.Local)
        return runner_class(context=self).run(command, **kwargs)
