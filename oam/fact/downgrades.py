#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
import pprint
import re
import click

from portage.versions import catpkgsplit

from oam.facts import facts
from oam.daylog import last_day, DayLog

# [ebuild     UD ] net-firewall/iptables-1.4.21-r1:0/0::gentoo [1.6.0:0/11::gentoo] USE="ipv6 netlink -conntrack -static-libs (-nftables%) (-pcap%)" 0 KiB
IS_DOWNGRADE = r'\s*\[ebuild[BNSRFUf #*~]+D[BNSRFUf #*~]+\]'

def package_name(line):
    return re.sub(r'^\[[^]]+\] ([^:]+).+', r'\1', line).strip()

def downgrade_version(line):
    split = catpkgsplit(package_name(line))
    return '{}-{}'.format(split[2], split[3])

def previous_version(line):
    return re.sub(r'^\[[^]]+\] [^:]+[^ ]+ \[([^\] ]+)\].+', r'\1', line).strip()
    
def process(filename):
    downgrades = {}
    with open(filename, 'r') as rdr:
        for line in rdr:
            if re.match(IS_DOWNGRADE, line) != None:
                downgrades[package_name(line)] = {
                    'line': line,
                    'to_version': downgrade_version(line),
                    'from_version': previous_version(line)
                    }

    return downgrades
                
def fact(day=last_day()):
    """Return a list of downgrades"""
    downgrades = {}
    for logfile in DayLog(day).runfiles('merge.log'):
        downgrades.update(process(logfile))
    return {
        'downgrades': downgrades
    }

@facts.command()
def downgrades():
    """A list of merge downgradess"""
    result = fact()
    print(pprint.pformat(result))
    return 0
