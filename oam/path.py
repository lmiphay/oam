# -*- coding: utf-8 -*-

import datetime
import os
import os.path
import time

OAM_LOGDIR = '/var/log/oam'

def timestamp():
    return time.strftime('%Y%m%d:%H:%M:%S')

def todays_dir():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')

def log_dir():
    return os.getenv('OAM_LOGDIR', OAM_LOGDIR) + '/' + todays_dir()

def make_log_dir():
    dirname = log_dir()
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    return dirname

def log_file(facility='oam'):
    filename = make_log_dir() + '/' + facility + '.log'
    if not os.path.isfile(filename):
        with open(filename, 'w') as f:
            f.write('{} created {} log file\n'.format(timestamp(), facility))
    return filename
