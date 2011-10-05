#!/usr/bin/env/python

from setuptools import setup

setup(
    name = 'ecl_twitter',
    version = '0.3.3',
    url = 'http://elmcitylabs.com',
    license = 'BSD',
    description = 'Easy Twitter integration for Django.',
    author = 'Dan Loewenherz',
    author_email = 'dan@elmcitylabs.com',
    packages=["ecl_twitter"],
    install_requires=["django==1.3"],
)

