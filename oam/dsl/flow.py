# -*- coding: utf-8 -*-

class Flow(object):

    def __init__(self, description=''): # **kwargs
        self.description = description
        self.hosts = Hosts()
        self.steps = Steps()

    def on(self, hosts):
        self.hosts.add(hosts)
        return self

    def add(self, steps):
        self.steps.add(steps)
        return self

