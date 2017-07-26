# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import yaml

OAM_EMERGE_OPTS = os.getenv('OAM_EMERGE_OPTS', '--backtrack=50 --deep --verbose --verbose-conflicts')
OAM_GO = os.getenv('OAM_GO', 'oam-flow weekly')
OAM_HEARTBEATSLEEP = os.getenv('OAM_HEARTBEATSLEEP', 5)
OAM_KEEPLOGS = os.getenv('OAM_KEEPLOGS', 10)
OAM_LOGDIR = os.getenv('OAM_LOGDIR', '/var/log/oam')
OAM_MULTITAIL_EXTRA_OPT = os.getenv('OAM_MULTITAIL_EXTRA_OPT', None)
OAM_REVIEW_HOSTS = os.getenv('OAM_REVIEW_HOSTS', 'localhost')
OAM_SANDBOXWAIT = os.getenv('OAM_SANDBOXWAIT', 8)
OAM_TS = os.getenv('OAM_TS', '%Y%m%d:%H:%M:%S')

PORTAGE_CONFIGROOT = os.getenv('PORTAGE_CONFIGROOT', '')

GLOBAL_CONFIG = '/etc/oam.yaml'

def dump():
    for var in dir(oam.settings):
        if var.startswith('OAM_') or var.startswith('PORTAGE_'):
            print(var, '=', getattr(oam.settings, var))

def get_setting(name, default_value=None):
    return getattr(sys.modules[__name__], name, default_value)

def get_flow(name):
    if os.path.exists(GLOBAL_CONFIG):
        config = yaml.load(open(GLOBAL_CONFIG))
        if type(config) is dict:
            if 'flows' in config:
                if name in config['flows']:
                    return config['flows'][name]
    return None
