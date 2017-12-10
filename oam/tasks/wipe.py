# -*- coding: utf-8 -*-

from invoke import task


@task(default=True, help={'spec': 'remove packages matching this pattern'})
def wipe(ctx, spec):
    """Mass package removal - e.g. "oam wipe 'kde*/*'" """
    ctx.run("emerge -C $(equery -qC list '{}' | sed -e 's/^/=/')".format(spec))
