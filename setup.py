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
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        ],
    install_requires=['requests', 'objectifier>=1.1.2'],
    package_data={'': ['LICENSE']},
)

