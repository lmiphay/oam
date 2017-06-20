# -*- coding: utf-8 -*-

import invoke

import clean
import depclean
import emptytree
import expire
import fetch
import flow
import glsa
import kernel
import layman
import newuse
import skel
import sync
import update

ns = invoke.Collection()

ns.add_collection(clean)
ns.add_collection(depclean)
ns.add_collection(emptytree)
ns.add_collection(expire)
ns.add_collection(fetch)
ns.add_collection(flow)
ns.add_collection(glsa)
ns.add_collection(kernel)
ns.add_collection(layman)
ns.add_collection(newuse)
ns.add_collection(skel)
ns.add_collection(sync)
ns.add_collection(update)
