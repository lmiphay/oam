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

OAM_CONFIG = os.getenv('OAM_CONFIG', '/etc/oam.yaml')

PORTAGE_CONFIGROOT = os.getenv('PORTAGE_CONFIGROOT', '')
PORTAGE_DISTFILES = os.getenv('PORTAGE_DISTFILES', '/usr/portage/distfiles')

def get_config():
    config = {}

    # set defaults
    for var in dir(sys.modules[__name__]):
        if var.startswith('OAM_'):
            config[var[4:].lower()] = getattr(sys.modules[__name__], var)

    # overwrite/load settings from config file
    if os.path.exists(OAM_CONFIG):
        config = yaml.load(open(OAM_CONFIG))

    # if present in the environment then overwrite
    for var in dir(sys.modules[__name__]):
        if var.startswith('OAM_'):
            if var in os.environ:
                config[var[4:].lower()] = os.getenv(var)

    return config

def dump():
    for var in dir(sys.modules[__name__]):
        if var.startswith('OAM_') or var.startswith('PORTAGE_'):
            print(var, '=', getattr(sys.modules[__name__], var))

def get_setting(name, default_value=None):
    return getattr(sys.modules[__name__], name, default_value)

def get_flow(name):
    config = get_config()
    if 'flows' in config:
        if name in config['flows']:
            return config['flows'][name]
    return None
