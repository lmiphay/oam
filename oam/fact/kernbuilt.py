# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import click

from oam.facts import facts
from oam.daylog import last_day, DayLog

def fact(day=last_day()):
    """Return the version of the newly built kernel (if any)"""
    kernel_log = '{}/kernel.log'.format(DayLog(day).day_dir())
    kernel_ver = None
    if os.path.isfile(kernel_log):
        for line in open(kernel_log):
            if 'DEPMOD' in line:
                kernel_ver = line.split()[1]
                break
    return {
        'kernel_built': kernel_ver
    }

@facts.command()
@click.option('--day', default=last_day(), help='day logs to process')
def kernbuilt(day):
    """Return kernel version build on specified day (if any)"""
    print(fact(day)['kernel_built'])
    return 0
