# -*- coding: utf-8 -*-

class Steps(object):

    def __init__(self, steps=[]):
        self.steps = steps

    def add(self, steps):
        self.steps.append(steps)
        return self
