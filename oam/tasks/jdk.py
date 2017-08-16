# -*- coding: utf-8 -*-

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

# in blocks and merge log files
MATCH = 'Oracle requires you to download the needed files manually after'

@task(default=True)
def fetch(ctx, version='8u144', dest='/usr/portage/distfiles'):
    """fetch the specified oracle jdk to the specified directory"""
    specific_url = oam.settings.jdk[version]
    ver = '{0}-{1}/jdk-{0}-linux-x64.tar.gz'.format(version, specific_url)
    with ctx.cd(dest):
        ctx.run('wget {} {} {}/{}'.format(oam.settings.jdk.opts, oam.settings.jdk.header, oam.settings.jdk.site, ver))
        ctx.run('chown portage:portage {}'.format(os.path.basename(ver)))
