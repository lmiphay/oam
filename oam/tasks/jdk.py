# -*- coding: utf-8 -*-

from __future__ import print_function
import os.path

from invoke import task

import oam.settings

"""
In /etc/oam/conf.d/jdk.yaml:

jdk:
  site: http://download.oracle.com/otn-pub/java/jdk
  header: '--header "Cookie: oraclelicense=accept-securebackup-cookie"'
  opts: '--continue --no-check-certificate --no-cookies'
  version: 8u152
  specific_url: b16/aa0333dd3019491ca4f6ddbe78cdb6d0
"""

# http://download.oracle.com/otn-pub/java/jdk/8u144-b01/090f390dda5b47b9b721c7dfaa008135/jdk-8u144-linux-x64.tar.gz
# http://download.oracle.com/otn-pub/java/jdk/8u151-b12/e758a0de34e24606bca991d704f6dcbf/jdk-8u151-linux-x64.tar.gz
# http://download.oracle.com/otn-pub/java/jdk/8u151-b12/e758a0de34e24606bca991d704f6dcbf/jdk-8u151-linux-x64.tar.gz
# http://download.oracle.com/otn-pub/java/jdk/8u152-b16/aa0333dd3019491ca4f6ddbe78cdb6d0/jdk-8u152-linux-x64.tar.gz

# in blocks and merge log files
MATCH = 'Oracle requires you to download the needed files manually after'

DIRECTORY = '/usr/portage/distfiles'

def jdk_filename():
    return 'jdk-{version}-linux-x64.tar.gz'.format(version=oam.settings.jdk.version)


def url():
    """http://download.oracle.com/otn-pub/java/jdk/8u151-b12/e758a0de34e24606bca991d704f6dcbf/jdk-8u151-linux-x64.tar.gz"""
    return '{site}/{version}-{specific_url}/{filename}'.format(site=oam.settings.jdk.site,
                                                               version=oam.settings.jdk.version,
                                                               specific_url=oam.settings.jdk.specific_url,
                                                               filename=jdk_filename())

@task
def chown(ctx, directory=DIRECTORY):
    ctx.run('chown portage:portage {directory}/{filename}'.format(directory=directory,
                                                                  filename=jdk_filename()),
            echo=True)


@task(default=True, post=[chown])
def fetch(ctx, directory=DIRECTORY):
    """fetch the oracle jdk to directory"""
    with ctx.cd(directory):
        ctx.run('wget {opts} {header} {url}'.format(opts=oam.settings.jdk.opts,
                                                    header=oam.settings.jdk.header,
                                                    url=url()),
                echo=True)

@task
def pretend(ctx):
    print(url())
