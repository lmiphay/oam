# -*- coding: utf-8 -*-

import os
import logging

# todo:
# 1. setup logging for subprocesses (file destinations and default level) - proxy for runner
# 2. for a particular target select an appropriate backend (e.g. invoke.Local or pyssh or pyexpect). -> inject a runner

#  prog = Program(config_class=x)
#  runner_class = self.config.get('runner', Local)

# 3. point at a particular tasks file? or a set of files/dirs -> config
# 4. parameterise some commands - pull from oam module (oam.param.x)
# 5. flags: not in lxc, must-not-fail, optional-but-warn, quiet-on-fail
# 6. parallel task execution

# 7. want to log the actual command
# 8. need to ansi filter some output
# 9. select line buffering
# 10. stop stdout buffering
# 11. pretend mode

def is_executable(filename):
    """Return True if file exists and is executable"""
    return os.path.isfile(filename) and os.access(filename, os.X_OK)

def check_for_executable(filename):
    """Check if file is an executable and log a warning if it is missing"""
    if not is_executable(filename):
        logging.warning('{} not found'.format(filename))
        return False
    return True

def opts(ident='merge', mergelog=True):
    return {
        'out_stream': get_logstream(ident),
        'err_stream': get_errstream('blocks'),
        'hide': True
        }

def is_update_available(atom):
    pass

def preserved_libs():
    pass

def oamrun(ctx, cmd, options):
    logger.info('running %s', cmd)
    if not ctx.pretend:
        ctx.run(cmd, options)

# OAM_CONFIG = {
#     'emerge_opts': ['OAM_EMERGE_OPTS', '--keep-going --backtrack=50 --deep --verbose --verbose-conflicts'],
#     }

# def config(item):
    
def oam_config(a):
    return ""

# # push/pop
# @task
# def push(ctx, logfile='merge', loglevel=logging.INFO):
#     # ctx.config.runner.logging(logfile, loglevel)
#     # out_stream=
#     #def run(ctx, cmd):
#     #    # watchers=[]
#     #    ctx.run(command=cmd, hide=True, out_stream=x.stdout, err_stream=x.stderr)
#     pass

# class OamLocal(invoke.runners.Local):
    
#     def __init__(self, context):
#         super(OamLocal, self).__init__(context)
        
#     def start(self, command, shell, env):
#        pass
