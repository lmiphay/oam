import logging
import pprint
import click
from .cmd import cli
from flowrunner import FlowRunner

LOGGER = logging.getLogger('oam.run')

@cli.command(name='run',
             context_settings=dict(ignore_unknown_options=True))
@click.option('--flow',      default='Default',   envvar='OAM_FLOW',
              help="flow(s) to run (comma seperated)")
@click.option('--host',      default='localhost', envvar='OAM_HOST',
              help="host(s) to run the flow on (comma seperated)")
@click.option('--container', default='',          envvar='OAM_CONTAINER',
              help="container(s) to run the flow on (comma seperated)")
@click.option('--remote',    default='',          envvar='OAM_REMOTE',
              help="remote host(s) to run the flow on (comma seperated)")
@click.option('--dryrun/--no-dryrun', default=False,
              help="show what would happen but don't actually do it")
@click.argument('extraopts', nargs=-1)
               # help="key=value pairs to pass to the flow(s)")
@click.pass_context
def runcmd(ctx, flow, host, container, remote, dryrun, extraopts):
    """Run a flow

       oam run [options] -- [extra flow-specific options]

       Example:

       oam run -- --verbose=True --no-sync --no-eix-sync
    """
    LOGGER.log(logging.INFO, 'run flow=%s', flow)
    LOGGER.log(logging.INFO, '    host=%s', host)
    LOGGER.log(logging.INFO, '    container=%s', container)
    LOGGER.log(logging.INFO, '    remote=%s', remote)
    LOGGER.log(logging.INFO, '    dryrun=%s', dryrun)
    LOGGER.log(logging.INFO, '    ctx=%s', ctx.args)
    LOGGER.log(logging.INFO, '    extraopts=%s', extraopts)

    config = {
        'flow': flow.split(','),
        'host': host.split(','),
        'container': container.split(','),
        'remote': remote.split(','),
        'dryrun': dryrun,
        'extraopts':  extraopts
    }
    
    for opt in extraopts:
        option = opt.strip('-').split('=', 2)
        if len(option)==1:
            config[option[0]] = None
        else:
            config[option[0]] = option[1]
            
    LOGGER.log(logging.INFO, '    config=%s', pprint.pformat(config))
            
    return FlowRunner(config).run()
