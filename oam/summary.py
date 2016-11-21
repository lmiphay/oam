#!/usr/bin/python

from __future__ import print_function
import sys
import os
import re
import subprocess
import logging
import yaml
import click
from .cmd import cli
from .daylog import DayLog, last_day
from .facts import write_facts
from .report import Report

@cli.command()
@click.option('--template', default='summary.jinja2', envvar='OAM_SUMMARY_TEMPLATE')
@click.option('--daydir', default=last_day())
@click.option('--force-facts-regen', default=False,
              help='force facts regeneration if it already exists')
def summary(template, daydir, force_summary_regen):
    """Summarise merge activity"""
    logger = logging.getLogger("oam.summary")

    fact_file = "{}/summary.yaml".format(daydir)

    if not os.path.exists(fact_file) or force_facts_regen:
        write_facts(daydir, fact_file)

    logger.info('generating summary report')

    print(Report().build([fact_file]).render(template))

    return 0
