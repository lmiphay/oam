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
  8u144: b01/090f390dda5b47b9b721c7dfaa008135
"""

# http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
# e.g.: http://download.oracle.com/otn-pub/java/jdk/8u144-b01/090f390dda5b47b9b721c7dfaa008135/jdk-8u144-linux-x64.tar.gz
# VER = '8u144-b01/090f390dda5b47b9b721c7dfaa008135/jdk-8u144-linux-x64.tar.gz'
# BASE_URL = 'http://download.oracle.com/otn-pub/java/jdk'
# HEADER = '--header "Cookie: oraclelicense=accept-securebackup-cookie"'
# OPTS = '--continue --no-check-certificate --no-cookies'
#
# http://download.oracle.com/otn-pub/java/jdk/8u151-b12/e758a0de34e24606bca991d704f6dcbf/jdk-8u151-linux-x64.tar.gz

# in blocks and merge log files
MATCH = 'Oracle requires you to download the needed files manually after'

def jdk_filename():
    return 'jdk-{version}-linux-x64.tar.gz'.format(version=oam.settings.jdk.version)


def url():
    """ http://download.oracle.com/otn-pub/java/jdk/8u151-b12/e758a0de34e24606bca991d704f6dcbf/jdk-8u151-linux-x64.tar.gz """
    return '{site}/{version}-{specific_url}/{filename}'.format(site=oam.settings.jdk.site,
                                                               version=oam.settings.jdk.version,
                                                               specific_url=oam.settings.jdk.specific_url,
                                                               filename=jdk_filename())

@task
def chown(ctx):
    ctx.run('chown portage:portage {filename}'.format(filename=jdk_filename()))


@task(default=True. post=[chown])
def fetch(ctx, directory='/usr/portage/distfiles'):
    """fetch the oracle jdk to directory"""
    with ctx.cd(directory):
        ctx.run('wget {opts} {header} {url}'.format(opts=oam.settings.jdk.opts,
                                                    header=oam.settings.jdk.header,
                                                    url=url()))
@task
def pretend(ctx):
    print(url())
