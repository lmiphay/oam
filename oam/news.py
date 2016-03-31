#!/usr/bin/python

from __future__ import print_function
import sys
import os
import logging
import click
import subprocess
import re
from .cmd import cli

"""
    Wrapper around: eselect news list
    The shell implementation of which is at: 
       /usr/share/eselect/modules/news.eselect
"""
class News(object):
    
    IS_UNREAD = r'  \[[0-9]+\]  N'

    def __init__(self):
        self.size = None
    
    def eselect_news(self, cmd=['list']):
        """Return a list of news items"""
        try:
            output = subprocess.check_output(['eselect', 'news'] + cmd)
        except subprocess.CalledProcessError as ex:
            output = ex.output
        return output.splitlines()

    def count(self, count_type='new'):
        if not self.size:
            self.size = int(self.eselect_news(['count', count_type])[0])
        return self.size

    def get_unread(self):
        """Previous shell implementation:
        #  [21]     2015-04-16  FFmpeg default
        #  [22]  N  2015-06-08  udev-init-scripts-29 important changes
        eselect news list | egrep '  \[[0-9]*\]  N'
        """
        self.size = 0
        for item in self.eselect_news():
            if re.match(self.IS_UNREAD, item):
                yield item.strip()
                self.size += 1

@cli.command(name='checknews')
@click.pass_context
def checknews(ctx):
    """List new gentoo news items"""
    for item in News().get_unread():
        print(item)
    return 0

@cli.command(name='new-news-count')
@click.pass_context
def countnewnews(ctx):
    """Count new gentoo news items"""
    print(News().count())
    return 0
