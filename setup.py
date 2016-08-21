from distutils.core import setup
from distutils.command.install_data import install_data

setup(name='oam',
      version='5.0',
      description='gentoo-oam implementation',
      author='Paul Healy',
      url='https://github.com/lmiphay/gentoo-oam',
      packages=['oam',
                'oam/dsl',
                'oam/eventparser',
                'oam/fact'
      ],
      scripts=['bin/oam'],
      data_files=[('share/gentoo-oam',
                   ['share/gentoo-oam-functions.sh',
                    'share/gentoo-oam-multitail.conf',
                    'share/oam-watch.help',
                    'share/summary.jinja2'
                   ]
      )]
      )
