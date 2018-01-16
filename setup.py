#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import os
import sys
from distutils.sysconfig import get_python_lib

from setuptools import find_packages, setup

version = '0.9.8.dev1'

extra_install_requires = []
if sys.version_info < (3,0):
    extra_install_requires.append('future')

setup(
    name='msurrogate',
    version=version,
    url='',
    author='Lee McCuller',
    author_email='Lee.McCuller@gmail.com',
    description=(
        'Interface With a python process from Matlab'
    ),
    license='Apache v2',
    packages=find_packages(exclude=['doc']),
    setup_requires = [
        'pytest-runner'
    ],
    install_requires = [
        'numpy',
        'Pyro4',
    ] + extra_install_requires,
    tests_require = [
        'pytest',
        'pytest-runner',
        'pytest-benchmark',
    ],
    zip_safe=False,
    keywords = 'Controls Linear Physics',
    classifiers=[
        'Development Status :: 3 - Alpha ',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)

