from distutils.core import setup
from distutils.command.install_data import install_data

setup(name='oam',
      version='5.0',
      description='oam implementation',
      author='Paul Healy',
      url='https://github.com/lmiphay/gentoo-oam',
      packages=['oam',
                'oam/eventparser',
                'oam/fact',
                'oam/oaminvoke',
                'oam/tasks'
      ],
      scripts=['bin/oam'],
      data_files=[('share/oam',
                   [
                    'share/oam-multitail.conf',
                    'share/oam-watch.help',
                    'share/summary.jinja2'
                   ]),
                  ('/etc/oam', ['etc/oam.yaml']),
                  ('/etc/oam/conf.d', ['conf.d/monthly.yaml',
                                       'conf.d/sync.yaml']),
                  ('/etc/oam/localtasks', ['localtasks/__init__.py',
                                           'localtasks/skel.py']),
                  ('/etc/cron.daily', ['etc/oam.cron']),
                  ('/etc/cron.monthly', ['etc/oam-depclean-check.cron']),
                  ('/usr/share/man/man8', ['man/oam.8'])
      ]
)
