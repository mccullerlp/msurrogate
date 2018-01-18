#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import os
import sys
from distutils.sysconfig import get_python_lib
from os import path
import warnings


from setuptools import find_packages, setup

version = '0.9.0.dev1'

def check_versions():
    try:
        curpath = path.abspath(path.realpath(os.getcwd()))
        setuppath = path.abspath(path.realpath(path.split(__file__)[0]))

        if curpath != setuppath:
            sys.path.append(setuppath)
        import msurrogate

        modfile = path.abspath(path.realpath(path.split(msurrogate.__file__)[0]))
        mod_relpath = path.relpath(modfile, setuppath)
        if mod_relpath == 'msurrogate':
            if msurrogate.__version__ != version:
                warnings.warn("Stated module version {0} different than setup.py version {1}".format(msurrogate.__version__, version))

        import subprocess
        try:
            git_tag = subprocess.check_output(['git', 'describe', '--tags', '--abbrev'])
        except subprocess.CalledProcessError:
            pass
        else:
            if git_tag != version:
                warnings.warn("latex git-tag different than setup.py version {1}".format(msurrogate.__version__, version))
    except ImportError:
        pass


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
    ],
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
    ],
)

