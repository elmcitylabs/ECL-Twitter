try:
    from django.conf import settings
    dir(settings)
except ImportError:
    import os
    class settings(object):
        TWITTER_KEY = os.environ.get('TWITTER_KEY')
        TWITTER_SECRET = os.environ.get('TWITTER_SECRET')
        TWITTER_REDIRECT_URL = os.environ.get('TWITTER_REDIRECT_URL')

import warnings
import urllib

KEY = getattr(settings, 'TWITTER_KEY', None)
SECRET = getattr(settings, 'TWITTER_SECRET', None)
REDIRECT_URL = getattr(settings, 'TWITTER_REDIRECT_URL', None)

if not all([KEY, SECRET, REDIRECT_URL]):
    warnings.warn("TWITTER_KEY, TWITTER_SECRET, and TWITTER_REDIRECT_URL must all be defined in your settings.py file or in your environment.", ImportWarning)

BASE_URL = 'https://api.twitter.com/'
INSECURE_URL = 'http://api.twitter.com/'

