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
      scripts=['bin/oam', 'bin/update-oam'],
      data_files=[('share/oam',
                   [
                    'share/oam-multitail.conf',
                    'share/oam-watch.help',
                    'share/summary.jinja2',
                    'share/summary-md.jinja2'
                   ]),
                  ('/etc/oam', [
                      'etc/oam.yaml',
                      'etc/oam.screenrc',
                  ]),
                  ('/etc/oam/conf.d', ['etc/conf.d/jdk.yaml',
                                       'etc/conf.d/monthly.yaml',
                                       'etc/conf.d/skel.yaml',
                                       'etc/conf.d/sync.yaml'
                  ]),
                  ('/etc/oam/localtasks', ['etc/localtasks/__init__.py',
                                           'etc/localtasks/skel.py']),
                  ('/etc/cron.daily', ['etc/cron.daily/oam']),
                  ('/usr/share/man/man8', ['man/oam.8',
                                           'man/oam-expire.8',
                                           'man/oam-flow.8',
                                           'man/oam-pretend.8',
                                           'man/oam-watch.8'
                  ])
      ]
)
