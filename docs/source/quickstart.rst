==========
Quickstart
==========

* First add the overlay::

    # layman -L && layman -a lmiphay

* After adding the overlay there is a keyword file at::

    /var/lib/layman/lmiphay/oam.keywords

  Add the contents to: ``/etc/portage/package.keywords``

* Then::

    # emerge app-oam/oam

* The `getoam.sh <https://raw.githubusercontent.com/lmiphay/oam/master/bin/getoam.sh>`_ script attempts to automate these steps.

* Review the default settings, make any local changes::

    # vi /etc/oam/oam.yaml

* And then kick off the default flow::

    # oam flow weekly

* In another terminal monitor progress with::

    # oam watch

* All logging takes place under::

    /var/log/oam/[TODAYS_DATE]

  You can browse the contents of that directory using `ranger(1) <http://ranger.nongnu.org/>`_
  from ``oam watch`` by typing: `Control-N`

  You can inspect the current list of ebuilds being merged by selecting the ``merge.log`` file in
  that directory (typing `Control-R` from ``oam watch`` will bring that up directly).

* When the ``oam flow weekly`` command returns check the ``error.log`` and ``blocks.log`` files.

* When the weekly flow completes typing `Control-U` from ``oam watch`` will bring up a simple summary
  log of everything that has taken place.

* There are two useful aliases for specific flows available::

    # oam go

  will run the flow specified in ``/etc/oam/oam.yaml`` (by default this is the ``weekly`` flow).

* The second alias::

    # oam resume

  will run the ``resume`` flow defined in ``/etc/oam/oam.yaml`` - by default this is the flow used
  to continue an update following a manual resolution of blockers, keyworking fixes, use flag changes... etc

