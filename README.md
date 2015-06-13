#### Table of Contents

* [Table of Contents](#table-of-contents)
* [Operations/Admin/Management for gentoo](#operationsadminmanagement-for-gentoo)
* [Workflows](#workflows)
* [Manual Operations](#manual-operations)
* [Features](#features)
* [Why should you not use gentoo-oam?](#why-should-you-not-use-gentoo-oam)
* [Known Similar Tools](#known-similar-tools)
* [Copyright](#copyright)

#### Operations/Admin/Management for gentoo

gentoo-oam aims to reduce some of the repetition of normal regular maintainance tasks on a gentoo server.

The philosophy is to:
+ automate tasks where it is safe to do so (e.g. merge blockers must be still resolved manually)
+ log all actions and outputs (to aid postmortum analysis and followup manual intervention)
+ provide a dashboard view of the progress of actions and results (to spot issues early)
+ provide an editor preloaded with logs and portage config files ("vim -p" tabs)

See `man 8 gentoo-oam` / gentoo-oam(8) for documentation.

#### Workflows

Workflows are a sequence of steps which are executed in sequence, stopping at the first failure.

For example the default weekly workflow will run these steps:

1. sync: `emaint --auto sync, layman --sync=ALL, eix-update/eix-remote`
2. glsa: `glsa-check`
3. fetch: `emerge --fetchonly --update world`
4. update: `emerge --update world, python-updater, perl-cleaner, emerge @preserved-rebuild`
5. clean: `eclean distfiles, eclean-kernel`
6. kernel: attempts to build a new kernel if necessary
7. qcheck: `qcheck --all`

From workflow specific configuration a complete step can be skipped,
or where it makes sense one of components of a step
(e.g. eclean-kernel, perl-cleaner... etc).

#### Manual Operations

The operator must still manually:

+ resolve keyword or use flag blockers (see the blocks.log file for a starting point)
+ run `dispatch-conf` when prompted/required
+ run `emerge --depclean`

#### Features

* simple workflow configuration on a per-server basis - new workflows can be added
* dashboard display of currently running oam processes
* logs all operations, errors, process output... etc
* install via ebuild from the [lmiphay overlay](https://gitweb.gentoo.org/user/lmiphay.git/about/)
* pulls in many useful dependencies as part of the install (eix, genlop, multitail, logrotate, eclean-kernel)

![oam-watch](screenshots/oam-watch2.png?raw=true "oam-watch sample")

#### Why should you not use gentoo-oam?

* it is not a way to become familar with gentoo (learn emerge... etc first)
* you are happy with your current workflow (stick with your own scripts)

#### Known Similar Tools

* [porticron](https://github.com/gentoo/porticron)
* [gentmaint](http://gentmaint.sourceforge.net/)
* [glcu](http://www.panhorst.com/glcu/)
* [ug](https://github.com/sidusnare/ug)
* [update](http://weaver.gentooexperimental.org/update.html)

#### Copyright

Copyright (c) 2013-2015 Paul Healy

Permission granted to redistribute it and/or modify it under the terms of the
GNU General Public License version 2.
