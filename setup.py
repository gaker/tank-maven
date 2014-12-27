#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def get_readme():
    return open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


def get_requirements():
    path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(path) as _file:
        requirements = _file.read().strip().split('\n')

    return requirements


setup(
    name='tank_maven',
    version='0.0.1',
    description='Web frontend for RaspberryPi-based Tank Controller',
    author='Greg Aker',
    author_email='greg@gregaker.net',
    license='BSD',
    packages=find_packages(),
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'tank-maven = tank_maven.main:main',
        ],
    },
)

