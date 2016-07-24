#!/usr/bin/python
# -*- coding: utf-8 -*-

import click
from .cmd import cli

@cli.group()
def facts():
    """Server/build information"""
    pass
