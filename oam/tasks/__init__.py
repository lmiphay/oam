# -*- coding: utf-8 -*-

import invoke

from oam.tasks import clean
from oam.tasks import config
from oam.tasks import depclean
from oam.tasks import eix
from oam.tasks import emptytree
from oam.tasks import expire
from oam.tasks import fetch
from oam.tasks import flow
from oam.tasks import gcc
from oam.tasks import glsa
from oam.tasks import jdk
from oam.tasks import kernel
from oam.tasks import layman
from oam.tasks import newuse
from oam.tasks import perl
from oam.tasks import qcheck
from oam.tasks import report
from oam.tasks import resume
from oam.tasks import skel
from oam.tasks import sync
from oam.tasks import update

ns = invoke.Collection()

ns.add_collection(clean)
ns.add_collection(config)
ns.add_collection(depclean)
ns.add_collection(eix)
ns.add_collection(emptytree)
ns.add_collection(expire)
ns.add_collection(fetch)
ns.add_collection(flow)
ns.add_collection(gcc)
ns.add_collection(glsa)
ns.add_collection(jdk)
ns.add_collection(kernel)
ns.add_collection(layman)
ns.add_collection(newuse)
ns.add_collection(perl)
ns.add_collection(qcheck)
ns.add_collection(report)
ns.add_collection(resume)
ns.add_collection(skel)
ns.add_collection(sync)
ns.add_collection(update)
