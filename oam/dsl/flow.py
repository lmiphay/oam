# -*- coding: utf-8 -*-

class Flow(object):

    def __init__(self, description=''): # **kwargs
        self.description = description
        self.hosts = Hosts()
        self.steps = Steps()
        self.run_detached = False

    def on(self, hosts):
        self.hosts.add(hosts)
        return self

    def perform(self, steps):
        self.steps.add(steps)
        return self

    def detach(self, run_detached=True):
        self.run_detached = run_detached

