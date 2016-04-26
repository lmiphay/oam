#!/usr/bin/python

from __future__ import print_function
import sys
import os
import logging
import click
import subprocess
import re
from .cmd import cli

IS_EBUILD = r'\s*\[ebuild'
IS_SUMMARY = r'\s*Total: '
IS_MERGE_RECORD = r'>>> ([-\w\./]+) merged\.'

""" Process one or more merge.log files and summarise the proposed/actual merges
"""
class Merges(object):

    def __init__(self):
        self.proposed_merges = set()
        self.proposed_merge_list = []
        self.actual_merges = set()
        self.summary = [] # e.g. 'Total: 1 package (1 reinstall), Size of downloads: 0 KiB'

    def check(self, line):
        if re.match(IS_EBUILD, line) != None and line not in self.proposed_merges:
            self.proposed_merges.add(line)
            self.proposed_merge_list.append(line.strip())
        elif re.match(IS_SUMMARY, line) != None:
            self.summary.append(line.strip())
        else:
            result = re.match(IS_MERGE_RECORD, line)
            if result != None:
                self.actual_merges.add(result.groups()[0])

    def process(self, filename):
        """ """
        with open(filename, 'r') as rdr:
            for line in rdr:
                self.check(line)

    def run(self, filenames):
        for filename in filenames:
            if os.path.isfile(filename):
                self.process(filename)
        return self

    def total_summary(self):
        return self.summary

    def actual(self):
        return self.actual_merges

    def proposed(self):
        return self.proposed_merge_list

    def report(self, proposed, actual, summary):
        all_flag = not (proposed or actual or summary)
        if proposed or all_flag:
            print('All proposed merges: {}'.format(str(len(self.proposed_merge_list))))
            for mrg in self.proposed():
                print(mrg)
        if actual or all_flag:
            print('All actual merges: {}'.format(str(len(self.actual_merges))))
            for mrg in self.actual():
                print(mrg)
        if summary or all_flag:
            print('Merge summary:')
            for msg in self.summary:
                print(msg)

@cli.command()
@click.option('--proposed', default=False, envvar='show proposed merges only')
@click.option('--actual', default=False, envvar='show actual merges only')
@click.option('--summary', default=False, envvar='show summary only')
@click.argument('mergefiles', nargs=-1)
def mergesummary(proposed, actual, summary, mergefiles):
    """Summarise merge activity"""
    Merges().run(mergefiles).report(proposed, actual, summary)
    return 0
