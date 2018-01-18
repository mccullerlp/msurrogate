"""
"""
from __future__ import division, print_function, unicode_literals

from os import path


version = '0.9.0'


def matlabpath():
    return path.abspath(path.split(__file__)[0])


from .meta_app import (
    SurrogateApp,
    cookie_setup,
)

from .subproc_server import (
    SurrogateSubprocess,
)
