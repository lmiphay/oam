#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import logging
import click
from oam.facts import facts

def fact(day=None):
    """Return information on the server"""
    host = os.uname()
    return { 'hostname': host[1], 'kernel': host[2] }

@facts.command()
def server():
    """The servername"""
    print(str(fact()))
    return 0
