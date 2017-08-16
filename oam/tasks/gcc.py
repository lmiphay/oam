# -*- coding: utf-8 -*-

from invoke import task

@task
def cpp11gcc5(ctx):
    """see: new item from 2015-10-22: GCC 5 Defaults to the New C++11 ABI"""
    ctx.run("revdep-rebuild --library 'libstdc++.so.6' -- --exclude gcc")
