# -*- coding: utf-8 -*-

from invoke import task, Collection

import update

ns = Collection(update, updateall=update.update)
