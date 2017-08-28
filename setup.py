from distutils.core import setup
from distutils.command.install_data import install_data

setup(name='oam',
      version='5.0',
      description='oam implementation',
      author='Paul Healy',
      url='https://github.com/lmiphay/oam',
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
                  ('/etc/oam/conf.d', ['etc/conf.d/monthly.yaml',
                                       'etc/conf.d/sync.yaml']),
                  ('/etc/oam/localtasks', ['etc/localtasks/__init__.py',
                                           'etc/localtasks/skel.py']),
                  ('/etc/cron.daily', ['etc/cron.daily/oam']),
                  ('/etc/cron.monthly', ['etc/cron.monthly/oam-depclean-check']),
                  ('/usr/share/man/man8', ['man/oam.8'])
      ]
)
