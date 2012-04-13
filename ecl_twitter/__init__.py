# -*- coding: utf-8 -*-

"""
ecl_twitter
~~~~~~~~~~~

:copyright: (c) 2012 Elm City Labs, LLC
:license: Apache 2.0, see LICENSE for more details.

"""

from .metadata import (
    __author__,
    __copyright__,
    __email__,
    __license__,
    __maintainer__,
    __version__,
)

from .twitter import Twitter, TwitterError
from .decorators import twitter_begin, twitter_callback

__all__ = [
    '__author__', '__copyright__', '__email__', '__license__',
    '__maintainer__', '__version__', 'Twitter', 'TwitterError',
    'twitter_begin', 'twitter_callback'
]
