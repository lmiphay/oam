# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import click

from oam.facts import facts
from oam.news import News

def fact(day=None):
    """Return a list of the unread news items"""
    return {
        'unread_news': [ x for x in News().get_unread() ]
    }

@facts.command()
def unreadnews():
    """Print list of unread news items"""
    print(fact()['unread_news'])
    return 0
