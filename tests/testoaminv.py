# -*- coding: utf-8 -*-

import unittest

import invoke
from invoke import task

from  oam.oaminvoke.context import Context

@task
def cd_test(ctx):
    with ctx.cd('/var/tmp'):
        return ctx.run('pwd').stdout.strip()

class OamInvTest(unittest.TestCase):

    def test_cd(self):
        self.assertEqual(cd_test(Context()), '/var/tmp')
