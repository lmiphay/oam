# -*- coding: utf-8 -*-

import os
import os.path
import shutil
import sys
import glob
import platform
import gzip

from invoke import task

HOSTNAME = platform.node()
RUNNING_KERNEL = platform.release() # e.g. '4.9.22-aufs'

LINUX_SRC = '/usr/src/linux'

CONFIG = '/usr/src/linux/.config'
REPO = '/usr/src/linux/kernel-config.git'

# look for a kernel config file in these locations
KERNEL_CONFIG = [
    '/usr/src/linux-{}/.config'.format(RUNNING_KERNEL),
    '/proc/config.gz',
    '/boot/config-{}'.format(RUNNING_KERNEL),
    '{}/{}'.format(REPO, HOSTNAME)
]

EFI_DIR = '/boot/efi/EFI/Boot'
KERNEL_IMAGE = 'arch/x86_64/boot/bzImage'


def kernel_release(srcdir=LINUX_SRC):
    """returns full kernel version, e.g. 4.12.12-gentoo"""
    return open('{}/include/config/kernel.release'.format(srcdir)).read().strip()

@task
def clean(ctx, srcdir=LINUX_SRC):
    ctx.run('make -C {} clean'.format(srcdir), echo=True)

@task
def module_rebuild(ctx):
    ctx.run('emerge @module-rebuild', echo=True)

@task(post=[module_rebuild])
def make(ctx, srcdir=LINUX_SRC):
    ctx.run('make -C {} all modules_install'.format(srcdir), echo=True)

@task(pre=[clean], post=[make])
def cleanall(ctx):
    pass

@task
def initrepo(ctx):
    if not os.path.isdir(REPO):
        os.makedirs(REPO)
        ctx.run('git init {}'.format(REPO), echo=True)

@task(initrepo)
def backup(ctx):
    shutil.copyfile(CONFIG, '{}/{}'.format(REPO, HOSTNAME))
    with ctx.cd(REPO):
        ctx.run('git add {}'.format(HOSTNAME), echo=True)
        ctx.run('git commit -m "{}/{}"'.format(HOSTNAME, usrsrc_kernel()), echo=True)

@task
def findconfig(ctx):
    for config in KERNEL_CONFIG:
        if os.path.isfile(config):
            with open(CONFIG, 'w') as outf:
                if config.endswith('.gz'):
                    shutil.copyfileobj(gzip.open(config, 'r'), outf)
                    break
                else:
                    shutil.copyfileobj(open(config, 'r'), outf)
                    break

@task(post=[backup])
def olddefconfig(ctx):
    ctx.run('make -C /usr/src/linux olddefconfig', echo=True)

@task
def configure(ctx):
    if os.path.isfile(CONFIG):
        return
    findconfig(ctx)
    if os.path.isfile(CONFIG):
        olddefconfig(ctx)
    else:
        raise RuntimeError('failed to find .config for {}'.format(CONFIG))

@task(default=True, pre=[configure])
def check_new_kernel(ctx):
    if not os.path.isdir('/lib/modules/{}'.format(kernel_release())):
        make(ctx)

def usrsrc_kernel():
    try:
        return os.readlink(LINUX_SRC)[len('linux-'):]
    except OSError as ex:
        sys.exit('a valid kernel was not found at {}'.format(ex))

def is_efi():
    return os.path.isdir(EFI_DIR) and os.path.isfile('/usr/sbin/efibootmgr')

def is_grub():
    """grub v0.97"""
    return os.path.isdir('/boot/grub/grub.conf') and os.path.isfile('/sbin/grub')

@task
def install_efi(ctx, srcdir=LINUX_SRC):
    krel = kernel_release(srcdir)
    with ctx.cd(srcdir):
        ctx.run('cp -p {bzimg} {efidir}/{tag}.efi'.format(bzimg=KERNEL_IMAGE, efidir=EFI_DIR, tag=krel), echo=True)
        ctx.run("efibootmgr --create --part 1 --label {tag} --loader '{sep}efi{sep}boot{sep}{tag}.efi'".format(krel=krel, sep='\\'), echo=True)

@task
def install_grub(ctx, srcdir=LINUX_SRC):
    """todo: edit grub.conf maybe?"""
    krel = kernel_release(srcdir)
    with ctx.cd(srcdir):
        ctx.run('cp -p {bzimg} /boot/{tag}'.format(bzimg=KERNEL_IMAGE, tag=krel), echo=True)

@task
def install(ctx, srcdir=LINUX_SRC):
    if is_efi():
        install_efi(ctx, srcdir)
    elif is_grub():
        install_efi(ctx, srcdir)

def version(directory):
    return os.path.basename(directory)[len('linux-'):]

def oldest():
    kernels = sorted(glob.glob('/usr/src/linux-*'))
    return version(kernels[0]) if len(kernels) > 0 else None

def kernel_package(ctx, kernel_version):
    """handle gentoo-sources, aufs-sources... etc """
    return ctx.run('qfile --quiet --nocolor /usr/src/linux-{}/Makefile'.format(kernel_version),
                   hide=True).stdout

def bootnum(kernel_version):
    return ctx.run('efibootmgr | grep {}'.format(kernel_version)).stdout.split()[0]

@task
def purgebins(ctx, kernel_version):
    """Remove the kernel and kernel modules of the specified kernel version.
       Also remove the EFI entry (on an EFI) server.
    """
    if is_efi():
        ctx.run('echo efibootmgr --bootnum {} --delete-bootnum'.format(bootnum(kernel_version)),
                echo=True)
    ctx.run('rm -rf /lib/modules/{}'.format(kernel_version), echo=True)
    ctx.run('rm -f {}/{}.efi'.format(EFI_DIR, kernel_version), echo=True)

@task
def unmerge(ctx, kernel_version):
    """unmerge the specified kernel source tree"""
    ctx.run('emerge -C ={}-{}'.format(kernel_package(ctx, kernel_version), kernel_version),
            echo=True)

@task
def purge(ctx, kernel_version=oldest()):
    """remove binaries and source tree of the specified kernel (if they exist). Does not remove
       binaries if the kernel is the one that is actually running.
    """
    if kernel_version is None:
        return
    if kernel_version != RUNNING_VERSION:
        purgebins(ctx, kernel_version)
    clean(ctx, 'linux-'.format(kernel_version))
    unmerge(ctx, kernel_version)
