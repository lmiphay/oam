#!/usr/bin/python

import fabric.contrib.files
from fabric.api import *

env.hosts = [ '192.168.1.100' ]

def if_missing_do(sentinel, cmd):
    if not fabric.contrib.files.exists(sentinel):
        run(cmd)

def is_dir(path):
    with settings(warn_only=True):
        return run('test -d ' + path).success

def is_file(path):
    with settings(warn_only=True):
        return run('test -f ' + path).success

def setup_layman(overlay):
    if_missing_do('/usr/bin/layman', 'emerge app-portage/layman')
    if_missing_do('/etc/portage/repos.conf', 'mkdir -p /etc/portage/repos.conf && layman-updater -R')
    if_missing_do('/var/lib/layman' + overlay, 'layman -a ' + overlay)
    run('layman -s ' + overlay)

def install_keywords():
    if not fabric.contrib.files.is_link('/etc/portage/package.keywords/gentoo-oam.keywords'):
        if is_file('/etc/portage/package.keywords'):
            run('mv /etc/portage/package.keywords /etc/portage/pre-oam-package.keywords')
        run('mkdir -p /etc/portage/package.keywords')
        run('ln -s /var/lib/layman/lmiphay/gentoo-oam.keywords /etc/portage/package.keywords/')
        if is_file('/etc/portage/pre-oam-package.keywords'):
            run('mv /etc/portage/pre-oam-package.keywords /etc/portage/package.keywords/')
@task
def bootstrap():
    setup_layman('lmiphay')
    install_keywords()
    run('emerge gentoo-oam')
    run('oam-go')

def installed(pkg):
    run('qlist --exact--quiet --installed ' + pkg)
    #app-portage/portage-utils:qfile

