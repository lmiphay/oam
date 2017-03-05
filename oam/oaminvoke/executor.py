# -*- coding: utf-8 -*-

from __future__ import print_function

import invoke

class Executor(invoke.Executor):

    def __init__(self, collection, config=None, core=None):
        super(OamExecutor, self).__init__(collection, config, core)

    def expand_calls(self, calls, config):
        ret = []
        for call in calls:
            if isinstance(call, invoke.Task):
                call = invoke.Call(task=call)
            print('Creating OamContext')
            call.context = OamContext(config=self.config_for(call, config))
            ret.extend(self.expand_calls(call.pre, config))
            ret.append(call)
            ret.extend(self.expand_calls(call.post, config))
        return ret
