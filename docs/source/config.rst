=============
Configuration
=============

* Configuration can be localised on a server by making changes under ``/etc/oam``.

* For a simple configuration update, a change to ``/etc/oam/oam.yaml`` is sufficient::

    ...
    oam:
      emerge:
        opts: '--backtrack=50 --deep --verbose --verbose-conflicts'
      go: weekly
    ...

  The above excerpt shows two oam settings - default options to ``emerge``, and the flow executed by
  the ``oam go`` command.

  For example to add the ``--newuse`` flag as a default option to ``emerge`` simply edit the file
  so that it looks like::

    ...
    oam:
      emerge:
        opts: '--newuse --backtrack=50 --deep --verbose --verbose-conflicts'
      go: weekly
    ...

  The format of the file must be maintained - see documentation on the yaml file format
  at: `www.yaml.org <http://www.yaml.org/>`_ .

* Extra configuration files can also be dropped into ``/etc/oam/conf.d/`` - they will be
  merged with, and can potentially overwrite overlapping configuration from ``/etc/oam/oam.yaml`` - for example to
  add a new flow called ``sync``, this file can be dropped into the directory as: ``/etc/oam/conf.d/sync.yaml``::

    flows:
      sync:
        - sync
        - glsa


* New invoke tasks can be added in ``/etc/oam/localtasks`` - for example this file
  dropped in as ``/etc/oam/localtasks/skel.py``::

    # -*- coding: utf-8 -*-
    from invoke import task

    @task(default=True)
    def skel(ctx):
        ctx.run('/bin/echo "hello world"', echo_result=True)

  Can be added to a flow or invoked directly as ``skel``::

    $ oam inv -l | grep skel
     'skel.skel': ['skel'],
    $ oam step skel
    hello world

    $
