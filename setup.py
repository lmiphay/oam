from distutils.core import setup
from distutils.command.install_data import install_data
import subprocess
import os

class oam_install(install_data):
    def run(self):
        install_data.run(self)
        subprocess.call(['make', 'DESTDIR=' + os.environ['ED'], 'install'])

setup(name='oam',
      version='5.0',
      description='gentoo-oam implementation',
      author='Paul Healy',
      url='https://github.com/lmiphay/gentoo-oam',
      packages=['oam'],
      scripts=['bin/oam'],
      cmdclass={"install_data": oam_install},
      data_files=[('share/gentoo-oam',
                   ['share/gentoo-oam-functions.sh',
                    'share/gentoo-oam-multitail.conf',
                    'share/oam-watch.help'
                   ]
      )]
      )
