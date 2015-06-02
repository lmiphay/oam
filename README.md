## gentoo-oam - Operations/Admin/Management Workflow for gentoo

See `man 8 gentoo-oam` / gentoo-oam(8) for documentation on this package.

gentoo-oam is a set of scripts which can take some of the repetition of
the normal regular maintainance of gentoo server(s). For example the default
weekly task will run these steps:

1. sync: `emaint --auto sync, layman --sync=ALL, eix-update/eix-remote`
2. glsa: `glsa-check`
3. fetch: `emerge --fetchonly --update world`
4. update: `emerge --update world, python-updater, perl-cleaner, emerge @preserved-rebuild`
5. clean: `eclean distfiles, eclean-kernel`
6. kernel: if a new kernel has been install an attempt to build it is made
7. qcheck: `qcheck --all`

From configuration a complete step can be skipped,
or where it makes sense one of components of a step
(e.g. eclean-kernel, perl-cleaner... etc).

The operator must still:

+ resolve keyword or use flag blockers
+ run `dispatch-conf` when required
+ run `emerge --depclean`

### Features

* simple workflow configuration on a per-server basis - new workflows can be added
* dashboard display of currently running oam processes
* logs all operations, errors, process output... etc
* install via ebuild from the [lmiphay overlay](https://gitweb.gentoo.org/user/lmiphay.git/about/)
* pulls in many useful dependencies as part of the install (eix, genlop, multitail, logrotate, eclean-kernel)

![oam-watch](screenshots/oam-watch.png?raw=true "oam-watch sample")

### Why should you not use gentoo-oam?

* its not a way to become familar with gentoo (learn emerge... etc first)
* you are happy with your current workflow (stick with your own scripts)

### Known Similar Tools

* [ug](https://github.com/sidusnare/ug)
* [update](http://weaver.gentooexperimental.org/update.html)

### Copyright

Copyright (c) 2013-2015 Paul Healy

Permission granted to redistribute it and/or modify it under the terms of the
GNU General Public License version 2.
