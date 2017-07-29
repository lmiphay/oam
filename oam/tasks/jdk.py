# -*- coding: utf-8 -*-

import os.path
from invoke import task

# http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html
# e.g.: http://download.oracle.com/otn-pub/java/jdk/8u144-b01/090f390dda5b47b9b721c7dfaa008135/jdk-8u144-linux-x64.tar.gz
VER = '8u144-b01/090f390dda5b47b9b721c7dfaa008135/jdk-8u144-linux-x64.tar.gz'
BASE_URL = 'http://download.oracle.com/otn-pub/java/jdk'

OPTS = '--continue --no-check-certificate --no-cookies'
HEADER = '--header "Cookie: oraclelicense=accept-securebackup-cookie"'

# in blocks and merge log files
MATCH = 'Oracle requires you to download the needed files manually after'

@task(default=True)
def fetch(ctx):
    """fetch the latest oracle jdk to distfiles directory"""
    with ctx.cd('/usr/portage/distfiles'):
        ctx.run('wget {} {} {}/{}'.format(OPTS, HEADER, BASE_URL, VER))
        ctx.run('chown portage:portage {}'.format(os.path.basename(VER)))
