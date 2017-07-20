#### Table of Contents
[![Documentation Status](https://readthedocs.org/projects/gentoo-oam/badge/?version=latest)](http://gentoo-oam.readthedocs.io/en/latest/?badge=latest)

* [Table of Contents](#table-of-contents)
* [Operations/Admin/Management for gentoo](#operationsadminmanagement-for-gentoo)
* [Workflows](#workflows)
* [Features](#features)
* [Copyright](#copyright)

#### Operations/Admin/Management for gentoo

gentoo-oam aims to reduce some of the repetition of normal regular maintainance tasks on a gentoo server.

The philosophy is to:
+ automate tasks where it is safe to do so (e.g. merge blockers must be still resolved manually)
+ log all actions and outputs (to aid postmortum analysis and followup manual intervention)
+ provide a dashboard view of the progress of actions and results (to spot issues early)
+ provide an editor preloaded with logs and portage config files ("vim -p" tabs)
+ provide a quick glance summary of merges, blocks and new news items

See the [docs](http://gentoo-oam.readthedocs.io/en/latest/) for details.

#### Workflows

Workflows are a sequence of steps which are executed in sequence, stopping
at the first failure (usually).

Each step consists of one or more tasks. Generally all tasks in a step must
complete successfully before the next step starts.

For example the `weekly` workflow will run these steps:

<dl>
<dt>sync  </dt> <dd><pre>emaint --auto sync, layman --sync=ALL, eix-update/eix-remote</pre></dd>
<dt>glsa  </dt> <dd><pre>glsa-check</pre></dd>
<dt>fetch </dt> <dd><pre>emerge --fetchonly --update world</pre></dd>
<dt>update</dt> <dd><pre>emerge --update world, python-updater, perl-cleaner, emerge @preserved-rebuild</pre></dd>
<dt>clean </dt> <dd><pre>eclean distfiles, eclean-kernel</pre></dd>
<dt>kernel</dt> attempts to build a new kernel if necessary
<dt>qcheck</dt> <dd><pre>qcheck --all</pre></dd>
<dl>

Steps (or tasks) can be skipped for a particular server (by configuration).

#### Features

* simple workflow configuration on a per-server basis - new workflows can be added
* dashboard display of currently running oam processes built on [multitail](https://www.vanheusden.com/multitail/)
* overall _summary_ of a merge (what merged succesfully, what didn't, glsa's, blockers, qcheck differences, unread news items... etc)
* logs all operations, errors, process output... etc
* multi-server support for starting and monitoring operations
* install via ebuild from the [lmiphay overlay](https://gitweb.gentoo.org/user/lmiphay.git/about/)

![oam-watch](screenshots/oam-watch4.png?raw=true "oam-watch sample")

#### Copyright

Copyright (c) 2013-2017 Paul Healy

Permission granted to redistribute it and/or modify it under the terms of the
GNU General Public License version 2.
