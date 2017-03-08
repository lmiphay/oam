# -*- coding: utf-8 -*-

import invoke

import clean
import depclean
import emptytree
import expire
import fetch
import glsa
import update

ns = Collection()

ns.add_collection(clean)
ns.add_collection(depclean)
ns.add_collection(emptytree)
ns.add_collection(expire)
ns.add_collection(fetch)
ns.add_collection(glsa)
ns.add_collection(update)
