from distutils.core import setup
from distutils.command.install_data import install_data
import subprocess
import os

class oam_install(install_data):
    def run(self):
        install_data.run(self)
        print("Running: " + str(os.environ))
        subprocess.call(['make', 'DESTDIR=' + os.environ['ED'], 'install'])
        print("Complete")

setup(name='oam',
      version='5.0',
      description='gentoo-oam implementation',
      author='Paul Healy',
      url='https://github.com/lmiphay/gentoo-oam',
      packages=['oam'],
      scripts=['bin/oam'],
      cmdclass={"install_data": oam_install},
      data_files=[('screenshots', ['screenshots/oam-watch4.png'])]
      )
