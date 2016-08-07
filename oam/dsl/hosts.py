# -*- coding: utf-8 -*-

class Hosts(object):

    def __init__(self, hosts=[]):
        self.hosts = hosts

    def add(self, hosts):
        self.hosts.append(hosts)
        return self
