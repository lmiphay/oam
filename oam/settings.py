# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import sys
import glob
import copy
import logging
import yaml
import pprint
from attrdict import AttrDict

"""
    configuration is sourced from:

    1. default values defined in this file module
    2. values loaded from configuration files under /etc/oam
    3. overridden values from the environment (if any; i.e. optional)

    access like: oam.settings.oam.go
"""

DEFAULTS = {
    'oam': {
        'config': '/etc/oam/oam.yaml',
        'emerge': {
            'log': '/var/log/emerge.log',
            'opts': '--backtrack=50 --deep --verbose --verbose-conflicts'
        },
        'go': 'oam flow weekly',
        'heartbeatsleep': 5,
        'logs': {
            'dir': '/var/log/oam',
            'keep': 10             # number of iterations of logs to keep
        },
        'review': {
            'hosts': [ 'localhost' ]
        },
        'sandboxwait': 8,
        'ts': '%Y%m%d:%H:%M:%S'
    },
    'helper': {
        'edit': '/usr/bin/xterm -e /usr/bin/vi',
        'mtab': '/usr/bin/xterm -e /usr/bin/vi -p',
        'term': '/usr/bin/xterm -e'
    },
    'multitail': {
        'extraopt': '',
        'layout': {
            'row1': 9,
            'row2': 9,
            'col1': 45,
            'col2': 40
        }
    },
    'portage': {
        'configroot': 'XXX',
        'distfiles': '/usr/portage/distfiles'
    }
}

class Settings(object): # types.ModuleType

    def __init__(self):
        #self.conf = copy.deepcopy(DEFAULTS)
        self.conf = AttrDict(DEFAULTS)
        self.load_config()
        #self.over_write(self.conf, '')
        logging.info('final config %s', pprint.pformat(self.conf))

    def merge(self, incoming, current):
        for k, v in incoming.iteritems():
            if k not in current:
                current[k] = v
            elif isinstance(v, dict):
                if isinstance(current[k], dict):
                    self.merge(v, current[k])
                else:
                    current[k] = v # assume over write is ok?

    def load_config(self):
        for filename in [ self.conf['oam']['config'] ] + sorted(glob.glob('/etc/oam/conf.d/*.yaml')):
            try:
                self.merge(AttrDict(yaml.load(open(filename))), self.conf)
            except IOError as ex:
                logging.info('failed to load %s', filename)

    def over_write(self, config, path):
        for k, v in config.iteritems():
            key = '{}_{}'.format(path, k.upper())
            if isinstance(v, dict):
                self.over_write(v, key)
            else:
                config[k] = os.getenv(key, v)

    def get_config(self):
        return self.conf

    def get_attr(self, config, elements):
        if len(elements) == 1:
            if elements[0] in self.conf:
                return config[elements[0]]
            else:
                return None
        else:
            return self.get_attr(config[elements[0]], elements[1:])

    def __getattr__(self, attr):
        logging.error('lookup %s', attr)
        print(1, self.conf)
        print(2, self.conf['portage']['configroot'], 3)
        print(4, self.conf.portage.configroot, 5)
        return self.get_attr(self.conf, attr.split('.'))

    def logdir(self):
        return self.conf['oam']['logs']['dir']

old_module = sys.modules[__name__]

SETTINGS = Settings()
SETTINGS.conf.logdir = SETTINGS.logdir

# https://mail.python.org/pipermail/python-ideas/2012-May/014969.html
#sys.modules [__name__] = Settings()
sys.modules [__name__] = SETTINGS.get_config()
