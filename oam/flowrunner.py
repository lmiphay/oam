import sys
import os
import logging

class Default(object):

    def __init__(self):
        self.logger = logging.getLogger('oam.flow')
        
    def execute(self, host):
        self.logger.log(logging.INFO, 'exec default on %s', host)

class FlowRunner(object):

    def __init__(self, config):
        self.logger = logging.getLogger('oam.flowrunner')
        self.config = config

    def run(self):
        for flow in self.config['flow']:
            for host in self.config['host']:
                self.logger.log(logging.INFO, 'running %s on %s', flow, host)
                globals()[flow]().execute(host)
                
        return 0
