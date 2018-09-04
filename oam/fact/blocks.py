# -*- coding: utf-8 -*-

from __future__ import print_function
import click

from oam.facts import facts
from oam.daylog import last_day, DayLog
from oam.blocks import Blocks

def fact(day=last_day()):
    """Return a list of blocks"""
    runfiles = DayLog(day).runfiles('blocks.log')
    blockers = Blocks().run(runfiles)
    return {
        'errors': blockers.misc,
        'build_fails': list(blockers.failed),
        'keyword_useflag': blockers.kw_use
    }

@facts.command()
def blocks():
    """A list of merge blocks"""
    result = fact()
    for topic in ['errors', 'build_fails', 'keyword_useflag']:
        print(topic, ':')
        for msg in result[topic]:
            print(msg)
    return 0
