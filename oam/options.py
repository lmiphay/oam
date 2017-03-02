# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import logging

def oam_config(opt):
    if opt == 'emerge_opts':
        return os.getenv('OAM_EMERGE_OPTS', '--backtrack=50 --deep --verbose --verbose-conflicts')
    elif opt == 'oam_go':
        return os.getenv('OAM_GO', 'oam-flow weekly')
    else:
        logging.error('unknown option %s', opt)
        return ""
