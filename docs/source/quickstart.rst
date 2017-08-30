==========
Quickstart
==========

* Install the program::

    # layman -L && layman -a lmiphay

  After adding the overlay there will be a keyword file at::

    /var/lib/layman/lmiphay/oam.keywords

  The contents should be added to: `/etc/portage/package.keywords`

  Then::

    # emerge oam

  The `getoam.sh <https://raw.githubusercontent.com/lmiphay/oam/master/bin/getoam.sh>`_ script attempts to run all of these steps.

* Review the default settings, make any local changes::

    # vi /etc/oam/oam.yaml

* And then kick off the default flow::

    # oam flow weekly

* In another terminal monitor progress with::

    # oam watch

* All logging takes place under::

    /var/log/oam/[TODAYS_DATE]

  You can browse the contents of that directory using `ranger(1)` from `oam watch` by typing: `Control-N`

  You can inspect the current list of ebuilds being merged by selecting the `merge.log` file in that directory (typing `Control-R` from `oam watch` will bring that up directly).

* When the ``oam flow weekly`` command returns check the error.log and blocks.log files.
