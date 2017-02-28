# -*- coding: utf-8 -*-

import invoke
import update

ns = invoke.Collection(update, updateall=update.update)
