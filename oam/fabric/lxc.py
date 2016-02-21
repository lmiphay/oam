#!/usr/bin/python

import logging
from fabric.api import *
from fabric.tasks import Task

"""
For the moment run like this:
   fab -f lxc.py -l
   fab -f lxc.py ls
"""
# add cache management workflow

class ListRunning(Task):
    """ list running lxc's"""

    name        = 'ls' # fabric task name

    def run(self):
        run('lxc-ls --active')

ls_instance = ListRunning()

class IpAddr(Task):
    """ show the ip addr of an lxc """

    name        = 'ipa' # fabric task name

    FILTER = "| grep 'inet '| awk '{ print $2}"
    #awk '/inet addr/{print substr($2,6)}'
    def run(self, name, iface='eth0'):
        run('lxc-attach --name ' + name + ' -- ip addr show ' + iface + self.FILTER)

ipa_instance = IpAddr()

class Create(Task):

    name        = 'create' # fabric task name

    # generic lxc-create
    CMD         = 'lxc-create --template=gentoo'
    CONFIG_PATH = '--lxcpath=/etc/lxc' # -P/--lxcpath, value=`lxc-config lxc.lxcpath`, default='/var/lib/lxc'
    ROOTFS_PATH = '--dir='             # --dir=DIR Place rootfs directory under DIR
    LOG         = '--logfile=/var/log/oam/lxc.log --logpriority=DEBUG'

    # gentoo specific
    STAGE3      = '--tarball=' # /lxc/stage3-amd64-20160218.tar.bz2 '
    PORTAGE     = '--portage-dir=/usr/portage'
    # ROOTFS_PATH = '--rootfs=/lxc' # duplicates generic --dir option...
    # FLUSH_CACHE = '--flush-cache'

    def __init__(self):
        pass

    def dummy_portage_snapshot(self):
        """
        never download the portage snapshot
        """
        run('mkdir -p /var/cache/lxc/gentoo') 
        run('mkdir touch /var/cache/lxc/gentoo/portage.tbz')

    def run(self, name, tarball):
        self.name = name
        self.cmd = self.CMD + '--name=' + name + ' ' + self.CONFIG_PATH
        self.cmd = self.cmd + ' ' + self.LOG
        
        self.cmd = self.cmd + ' -- '
        
        self.cmd = self.cmd + self.PORTAGE
        self.cmd = self.cmd + self.STAGE3 + ' ' + tarball
        
        self.dummy_portage_snapshot()
        run(self.cmd)

create_instance = Create()

# The default configuration used for all containers at creation time is taken from
# /etc/lxc/default.conf
# => rootfs of container is : /lxc/oam2/rootfs
# => config of container is : /lxc/oam2/config
# -f, --config=file  Initial configuration file
# -p|--path)             path=$2; shift 2;;
# run('ln -s /lxc/oam2/config .')

class Start(Task):
    
    name        = 'start' # fabric task name
    
    CMD         = 'lxc-start --name='
    CONSOLE_LOG = '--console-log=/var/log/oam/console.log.'
    # FOREGROUND  = '--foreground'
    
    def __init__(self):
        pass

    def run(self, name):
        self.cmd = self.CMD + name + ' ' + self.CONSOLE_LOG + name
        run(self.cmd)

start_intance = Start()

class Stop(Task):
    
    name        = 'stop' # fabric task name
    
    CMD         = 'lxc-stop --name='

stop_instance = Stop()

class Destroy(Task):

    name        = 'destroy' # fabric task name
    
    CMD         = 'lxc-destory --force --name='

destroy_instance = Destroy()
