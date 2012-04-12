#!/usr/bin/env/python

import ecl_twitter

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = 'ecl_twitter',
    version = ecl_twitter.__version__,
    url = 'http://elmcitylabs.com',
    license = ecl_twitter.__license__,
    description = 'Easy Twitter integration for Django.',
    author = ecl_twitter.__author__,
    author_email = ecl_twitter.__email__,
    packages=['ecl_twitter'],
    install_requires=['django>=1.3', 'requests', 'objectifier>=1.1.2'],
    package_data={'': ['LICENSE']},
)

