from setuptools import setup
import os
import sys

_here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(_here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

version = {}
with open(os.path.join(_here, 'soundboard', 'version.py')) as f:
    exec(f.read(), version)

setup(
    name='soundboard',
    version=version['__version__'],
    description=('app for a Raspi to be a Soundboard'),
    author='Jeff Derksen',
    author_email='jeff.a.derksen@gmail.com',
    url='https://github.com/Jerksen/soundboard',
    license='GPL-3.0',
    packages=['soundboard'],
    install_requires=[  'toml',
                        'Pillow',
                        ''],
    include_package_data=True,
    )
