from distutils.core import setup
from distutils.command.install_data import install_data
import subprocess

class oam_install(install_data):
    def run(self):
        install_data.run(self)
        print("Running")
        # , cwd=os.path.join(dir, 'packagename')
        subprocess.call(['make', 'install'])
        print("Complete")

setup(name='oam',
      version='5.0',
      description='gentoo-oam implementation',
      author='Paul Healy',
      url='https://github.com/lmiphay/gentoo-oam',
      packages=['oam'],
      scripts=['bin/oam'],
      cmdclass={"install_data": oam_install},
      )
