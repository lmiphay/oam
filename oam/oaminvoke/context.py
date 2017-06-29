# -*- coding: utf-8 -*-

from __future__ import print_function

import invoke

import oam.lib
import oam.logdest

class Context(invoke.Context):

    def __init__(self, config=None):
        super(Context, self).__init__(config)

    def run(self, command, **kwargs):
        """ add oam flags: if_installed, pretend, echo_result """
        pretend = kwargs.pop('pretend', False)
        if_installed = kwargs.pop('if_new_rev', False)
        echo_result = kwargs.pop('echo_result', False)

        if pretend or (if_installed and not oam.lib.check_for_executable(command.split()[0])):
            return invoke.Result(command=command)
        else:
            kwargs['out_stream'], kwargs['err_stream'] = oam.logdest.logdest(command)

            if 'capture_buffer_size' in kwargs and kwargs['capture_buffer_size'] == -1:
                kwargs['capture_buffer_size'] = None
            elif not 'capture_buffer_size' in kwargs or not kwargs['capture_buffer_size']:
                kwargs['capture_buffer_size'] = 200

            runner_class = self.config.get('runner', invoke.Local)

            result = runner_class(context=self).run(command, **kwargs)

            if echo_result:
                print(result.stdout) # note now setting 'capture_buffer_size'

            return result

    def emerge(self, args, **kwargs):
        """ add oam flag: if_new_rev=bool """
        if_new_rev = kwargs.pop('if_new_rev', None)

        command = '/usr/bin/emerge {}'.format(args)

        if if_new_rev:
            if oam.lib.is_update_available(args.split()[-1]):
                return self.run(command, **kwargs)
            else:
                return invoke.Result(command=command)
        else:
            return self.run(command, **kwargs)
