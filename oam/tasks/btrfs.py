# -*- coding: utf-8 -*-
#
"""
"""
from __future__ import print_function

import glob
import yaml
from invoke import task
from invoke.tasks import call

# sys-fs/btrfsmaintenance
# https://btrfs.wiki.kernel.org/index.php/Manpage/btrfs(5)#MOUNT_OPTIONS
# https://btrfs.wiki.kernel.org/index.php/Main_Page
# https://btrfs.wiki.kernel.org/index.php/Problem_FAQ#I_get_.22No_space_left_on_device.22_errors.2C_but_df_says_I.27ve_got_lots_of_space

@task
def balance(ctx, filesystem):
    """
    see: https://btrfs.wiki.kernel.org/index.php/SysadminGuide#Balancing
    blocks. logs kernel messages like:
    ...
    Jan  2 18:53:54 mur kernel: BTRFS info (device sda1): found 4484 extents
    Jan  2 18:53:56 mur kernel: BTRFS info (device sda1): found 4484 extents
    Jan  2 18:53:56 mur kernel: BTRFS info (device sda1): relocating block group 104408809472 flags metadata

    example run:

    # btrfs balance start -musage=50 -dusage=50 /
    Done, had to relocate 18 out of 46 chunks
    #
    """
    ctx.run('btrfs balance start -musage=50 -dusage=50 {}'.format(filesystem), echo=True)

@task
def scrub(ctx, filesystem):
    """
    see: btrfs-scrub(1), non-blocking (unless -B passed), example run:

    # btrfs scrub start /
    scrub started on /, fsid 93263726-ae94-4d14-9dc2-8f7c4d2a6ca7 (pid=16672)
    #
    # btrfs scrub status /
    scrub status for 93263726-ae94-4d14-9dc2-8f7c4d2a6ca7
            scrub started at Tue Jan  2 18:58:00 2018 and finished after 00:00:55
            total bytes scrubbed: 23.60GiB with 0 errors
    #
    """
    ctx.run('btrfs scrub -B start {}'.format(filesystem), echo=True)

@task
def report(ctx, filesystem):
    ctx.run('btrfs filesystem df {}'.format(filesystem))
    ctx.run('btrfs filesystem show {}'.format(filesystem))
    ctx.run('btrfs scrub status {}'.format(filesystem))

@task(post=[report])
def maint(ctx, filesystem):
    balance(ctx, filesystem)
    scrub(ctx, filesystem)
    report(ctx, filesystem)
