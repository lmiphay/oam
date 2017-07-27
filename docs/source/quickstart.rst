=========
Quickstart
=========

``# layman -L && layman -a lmiphay``

After adding the overlay there will be a keyword file at: `/var/lib/layman/lmiphay/gentoo-oam.keywords`

``# emerge gentoo-oam``

Review the default settings, make any local changes:

``# vi /etc/oam.yaml``

And then kick off the default flow:

``# oam flow weekly``

In another terminal monitor progress with:

``# oam watch``

When the ``oam flow weekly`` command returns, browse to the set of log files generated under:
``/var/log/oam/[DATE]`` (start with the summary.log file).
