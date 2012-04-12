# -*- coding: utf-8 -*-

"""
ecl_twitter
~~~~~~~~~~~

:copyright: (c) 2012 Elm City Labs, LLC
:license: Apache 2.0, see LICENSE for more details.

"""

try:
    from .twitter import Twitter
    __all__ = ['Twitter']
except ImportError:
    # One of the required libraries hasn't been installed yet.
    pass

__version__ = "1.0.5"
__author__ = "Dan Loewenherz"
__copyright__ = "Copyright 2012, Elm City Labs, LLC"
__maintainer__ = "Dan Loewenherz"
__email__ = "dan@elmcitylabs.com"
__license__ = "Apache 2.0"

