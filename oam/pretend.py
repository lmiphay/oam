# -*- coding: utf-8 -*-

import sys
import os
import subprocess
import logging
import re
import click
from .cmd import cli

""" A wrapper around emerge --update --pretend world, which filters some noise out and
    in addition produces an ordered list of the packages which would be merged in a format
    suitable for feeding back into emerge.
"""
class Pretend:
    
    CMD = ['emerge', '--update', '--backtrack=50', '--deep', '--pretend', '-v']

    SKIPLINES = {
        'These are the packages that would be merged, in order:',
        'Total: 0 packages, Size of downloads: 0 KiB',
        ' * Use eselect news read to view new items.',
        ''
        }

    def __init__(self, target = 'world'):
        self.target = target
        self.logger = logging.getLogger("oam.pretend")
        self.packages = set()

    def filter(self, line):
        return line in self.SKIPLINES or line.startswith('Calculating dependencies')

    def add_package_name(self, line):
        """ parse emerge output for package specifiers; e.g.
              [ebuild     U ~] media-video/nvidia-settings-355.11::gentoo....
            ignore these type of records:
              [uninstall     ] dev-python/dnspython-1.11.1::gentoo....
              [blocks b      ] dev-python/dnspython:0....
        """
        if line.startswith('[ebuild'):
            self.packages.add(re.sub(r'^\[[^]]+\] ([^:]+).+', r'=\1', line))

    def dump_packages(self):
        if len(self.packages) > 0:
            print('Sorted merge list:')
            for pkg in self.packages:
                print(pkg)

    def run(self):
        self.logger.log(logging.DEBUG, 'pretend cmd: %s', str(self.CMD))
        self.logger.log(logging.DEBUG, 'running pretend for: %s', self.target)
        try:
            proc = subprocess.Popen(self.CMD + [self.target],
                                    bufsize=1,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
            for line in proc.stdout:
                if not self.filter(line):
                    print(line)
                    self.add_package_name(line)
            result = proc.wait()
            if result != 0:
                self.logger.log(logging.ERROR, 'pretend returned: %d', result)
        except (OSError, ValueError) as e:
            self.logger.log(logging.ERROR, 'pretend failed for: %s', self.target)
            self.logger.log(logging.ERROR, 'failure: %s', str(e))
        self.dump_packages()

@cli.command()
@click.argument('target')
def pretend(target):
    """emerge -up <target> (filtering noise)"""
    Pretend(target).run()
