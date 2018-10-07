# -*- coding: utf-8 -*-
"""
"""

import glob
import os
import subprocess

from invoke import task, call

WEBAPPS   = '/var/lib/tomcat-9/webapps'

GROK_SRC  = '/var/opengrok/src'
GROK_DATA = '/var/opengrok/data'
GROK_CFG  = '/var/opengrok/etc/configuration.xml'

GROK_BIN  = '/opt/opengrok/bin'
GROK_LIB  = '/opt/opengrok/lib'

INDEXER   = 'indexer.py -j /usr/bin/java -a {lib}/opengrok.jar '.format(lib=GROK_LIB)
CONFIG    = '--source {src} --dataRoot {data} --writeConfig {cfg} '.format(lib=GROK_LIB, src=GROK_SRC, data=GROK_DATA, cfg=GROK_CFG)
APP       = 'http://localhost:8080'

GROK_PATH = {'PATH': '{grok_bin}:{path}'.format(grok_bin=GROK_BIN, path=os.getenv('PATH'))}

def java_home():
    """ to select the java use e.g.:
        eselect java-vm set user oracle-jdk-bin-1.8
    """
    return subprocess.check_output('java-config-2 -O', shell=True).strip()


def repos():
    return [ x[len(GROK_SRC)+1:-5] for x in glob.glob('{}/*/.git'.format(GROK_SRC)) ]


@task
def deploy(ctx):
    """To be run after each new opengrok version is installed"""
    ctx.run('deploy.py {lib}/source.war {webapps}'.format(lib=GROK_LIB, webapps=WEBAPPS),
            env=GROK_PATH,
            echo=True)


@task
def pull(ctx):
    for repo in repos():
        with ctx.cd('{}/{}'.format(GROK_SRC, repo)):
            ctx.run('git pull', echo=True)


@task
def restarttomcat(ctx):
    ctx.sudo('/etc/init.d/tomcat-9 restart', echo=True)


@task(post=[restarttomcat])
def index(ctx):
    """
    See: https://github.com/oracle/opengrok/wiki/How-to-setup-OpenGrok
    """
    ctx.run(INDEXER +
            '-- ' +
            CONFIG +
            '--history '  +  # enable history
            '--projects ' +  # Generate a project for each top-level directory in source root
            '--search '   +  # Search for "external" source repositories and add them                ???
            '--assignTags ' +  # Assign commit tags to all entries in history for all repositories   ???
            '--uri {app}'.format(app=APP),
            env=GROK_PATH,
            echo=True)


@task(default=True, pre=[pull], post=[index])
def grok(ctx):
    pass


