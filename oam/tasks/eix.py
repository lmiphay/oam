# -*- coding: utf-8 -*-

"""
See: eix(1) and https://wiki.gentoo.org/wiki/Eix
"""

from invoke import task

@task(aliases=['eix-update'])
def update(ctx):
    """create eix's cache from the local portage and overlays
       to keep existing remote data set: KEEP_VIRTUALS=true  (or add to /etc/eixrc )
    """
    ctx.run('eix-update --nocolor --nostatus', env = {'KEEP_VIRTUALS': 'true'})

@task(aliases=['eix-remote'])
def remote(ctx):
    """ Executes these steps:
          1. get eix cache from gpo.zugaina.org (see fetch)
          2. store locally as /var/cache/eix/remote.tar.bz2
          3. merge the remote data into the local main eix db (see add)
    """
    ctx.run('eix-remote -H update') # -H = --nostatus

@task
def fetch(ctx):
    """Execute the fetch (only) of remote cache data - [eix-remote covers this]
       stores into /var/cache/eix/remote.tar.bz2 
    """
    ctx.run('eix-remote fetch')

@task
def add(ctx):
    """ Merge previously fetched remote data into the existing local eix db. 
        [eix-remote covers this]
    """
    ctx.run('eix-remote add')
