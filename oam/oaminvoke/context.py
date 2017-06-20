# -*- coding: utf-8 -*-

import logging
import invoke

import oam.lib
import oam.logdest

class Context(invoke.Context):

    def __init__(self, config=None):
        super(Context, self).__init__(config)

    def run(self, command, **kwargs):
        """ add oam flags: if_installed, pretend """
        logging.info('run %s', command)

        pretend = kwargs.pop('pretend', False)
        if_installed = kwargs.pop('if_new_rev', False)

        if pretend or (if_installed and not oam.lib.check_for_executable(command.split()[0])):
            return Result(command=command)
        else:
            kwargs['out_stream'], kwargs['err_stream'] = oam.logdest.LOGSUPERVISOR.logdest(command)
            runner_class = self.config.get('runner', invoke.Local)
            return runner_class(context=self).run(command, **kwargs)

    def emerge(self, args, **kwargs):
        """ add oam flag: if_new_rev=bool """
        command = '/usr/bin/emerge {}'.format(args)
        logging.info('emerge %s', command)

        if_new_rev = kwargs.pop('if_new_rev', None)
        if if_new_rev and oam.lib.is_update_available(args.split()[-1]):
            return self.run(cmd, kwargs)
        else:
            return Result(command=command)
