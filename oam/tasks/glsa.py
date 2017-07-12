# -*- coding: utf-8 -*-

import logging

import invoke
from invoke import task

class IssueChecker(invoke.watchers.StreamWatcher):

    def __init__(self):
        super(IssueChecker, self).__init__()
        self.count = 0

    def submit(self, stream):
        if '[N]' in stream:
            logger.warn('GLSA: %s', stream)
            self.count += 1
        return []

    def report(self):
        if self.count>0:
            logger.warn('GLSA: found %d issues', count)

# glsa dumps these lines to stderr, while the actual report goes to stdout.
#
# [A] means this GLSA was marked as applied (injected),
# [U] means the system is not affected and
# [N] indicates that the system might be affected.
# This system is affected by the following GLSAs:

@task(default=True)
def check(ctx):
    checker = IssueChecker()
    ctx.run('glsa-check --test --verbose --nocolor all', watchers=[checker])
    checker.report()
