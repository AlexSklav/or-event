#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from glob import glob
from os.path import basename
from os.path import splitext
from setuptools import find_packages
from setuptools import setup

import versioneer

# See https://blog.ionelmc.ro/2014/06/25/python-packaging-pitfalls/
setup(name='or-event',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description='Wait on multiple threading.Event instances',
      keywords='',
      author='Christian Fobel',
      author_email='christian@fobel.net',
      url='https://github.com/sci-bots/or-event',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
      # Install data listed in `MANIFEST.in`
      include_package_data=True)
