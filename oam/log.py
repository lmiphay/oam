import sys
import os
import logging
import click
import subprocess
import re
import datetime
from .cmd import cli

def todays_dir():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')

def logdir():
    return os.getenv('OAM_LOGDIR', '/var/log/oam') + todays_dir()

def get_logfile(facility):
    dirname = logdir()
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    filename = dirname + '/' + facility + '.log'
    if not os.path.isfile(filename):
        logmsg(filename, "created log file")
    return filename

"""
"""
class Log(object):

    def __init__(self, facility='oam'):
        self.logger = logging.getLogger("oam.log")
        self.fh = logging.FileHandler(get_logfile(facility))
        self.form = logging.Formatter(fmt='%(asctime)s %(message)s')
        self.fh.setFormatter(self.form)
        self.logger.addHandler(self.fh)

    def msg(self, tag, msgtext):
        self.logger.info('oam %(tag)s %(msgtext)s', tag=tag, msgtest=msgtext)
