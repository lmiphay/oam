#### Table of Contents

* [Table of Contents](#table-of-contents)
* [Operations/Admin/Management for gentoo](#operationsadminmanagement-for-gentoo)
* [Workflows](#workflows)
* [Quickstart](#quickstart)
* [Manual Operations](#manual-operations)
* [Features](#features)
* [Why should you not use gentoo-oam?](#why-should-you-not-use-gentoo-oam)
* [Prior Art](#prior-art)
* [Copyright](#copyright)

#### Operations/Admin/Management for gentoo

gentoo-oam aims to reduce some of the repetition of normal regular maintainance tasks on a gentoo server.

The philosophy is to:
+ automate tasks where it is safe to do so (e.g. merge blockers must be still resolved manually)
+ log all actions and outputs (to aid postmortum analysis and followup manual intervention)
+ provide a dashboard view of the progress of actions and results (to spot issues early)
+ provide an editor preloaded with logs and portage config files ("vim -p" tabs)
+ provide a quick glance summary of merges, blocks and new news items

See: gentoo-oam(8), oam-flow(8), oam-watch(8) for detailed documentation.

See [gentoo-koam](https://github.com/lmiphay/gentoo-koam) for a GUI over gentoo-oam to help cross-server monitoring.

Stub [docs](http://gentoo-oam.readthedocs.io/en/latest/) in progress.

#### Quickstart

```
# layman -L && layman -a lmiphay
```

After adding the overlay there will be a keyword file at: `/var/lib/layman/lmiphay/gentoo-oam.keywords`

```
# emerge gentoo-oam
```

Review the default settings, make any local changes, and then kick off the default flow:

```
# vi /etc/gentoo-oam.conf /etc/gentoo-oam.d/weekly.conf
# oam go
```

In another terminal monitor progress with:

```
# oam watch
```

When `oam go` returns, browse to the set of log files generated under:
`/var/log/oam/[DATE]` (start with the summary.log file).

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

#### Manual Operations

You must still manually:

+ resolve keyword or use flag blockers (see the blocks.log file for a starting point)
+ run `dispatch-conf` when prompted
+ remove obsolete packages manually with: `emerge --depclean`

#### Features

* simple workflow configuration on a per-server basis - new workflows can be added
* dashboard display of currently running oam processes built on [multitail](https://www.vanheusden.com/multitail/)
* overall _summary_ of a merge (what merged succesfully, what didn't, glsa's, blockers, qcheck differences, unread news items... etc)
* logs all operations, errors, process output... etc
* multi-server support for starting and monitoring operations
* install via ebuild from the [lmiphay overlay](https://gitweb.gentoo.org/user/lmiphay.git/about/)
* pulls in many useful dependencies as part of the install (eix, genlop, multitail, logrotate, ranger)
* bash shell completion support with [app-shells/bash-completion](http://bash-completion.alioth.debian.org/)

![oam-watch](screenshots/oam-watch4.png?raw=true "oam-watch sample")

#### Why should you not use gentoo-oam?

* it is not a way to become familar with gentoo (learn emerge... etc first)
* you are happy with your current workflow (stick with your own scripts)

#### Prior Art

* [ansible portage module](http://docs.ansible.com/ansible/portage_module.html)
* [gentoo-upsys](https://github.com/Krishath/gentoo-upsys)
* [porticron](https://github.com/gentoo/porticron)
* [gentmaint](http://gentmaint.sourceforge.net/)
* [glcu](http://www.panhorst.com/glcu/)
* [ug](https://github.com/sidusnare/ug)
* [update](http://weaver.gentooexperimental.org/update.html)
* [update-system.sh - tip 2](http://gentoovps.net/gentoo-portage-tips/)
* [autoupdating on reddit](https://www.reddit.com/r/Gentoo/comments/3w2od1/update_gentoo_autoupdating/)
* [linux config scripts](https://github.com/jappeace/linux-config/tree/master/scripts)
* [gentoo-sources-compilation-helper](https://github.com/rewtnull/gentoo-sources-compilation-helper)

#### Copyright

Copyright (c) 2013-2017 Paul Healy

Permission granted to redistribute it and/or modify it under the terms of the
GNU General Public License version 2.
