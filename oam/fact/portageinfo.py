# -*- coding: utf-8 -*-

from __future__ import print_function
import pprint
import click

from oam.facts import facts
from oam.pkg import Pkg

def fact(day=None):
    """Return info on/from the installed portage package"""
    p = Pkg()
    return {
        'installed_version': p.current_version('sys-apps/portage'),
        'best_available': p.best_available('sys-apps/portage'),
        'update_available': p.is_update_available('sys-apps/portage'),
        'preserved_libs': p.preserved_libs()
    }

@facts.command()
def portageinfo():
    """Information on/from the installed portage"""
    result = fact()
    print(pprint.pformat(result))
    return 0
