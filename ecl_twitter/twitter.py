import random
import time
import hmac
import hashlib
import urllib
import urlparse
import uuid
from operator import itemgetter

try:
    import requests
except ImportError:
    import urllib2

    class Response(object):
        def __init__(self, data, headers):
            self.text = data
            self.headers = headers


    class requests(object):
        @staticmethod
        def post(url, data, headers):
            encoded_params = "&".join("%s=%s" % (k, v) \
                    for k, v in data.iteritems())
            request = urllib2.Request(url, encoded_params, headers)
            response = urllib2.urlopen(request)
            return Response(response.read(), response.headers)

        @staticmethod
        def get(url, params, headers):
            encoded_params = "&".join("%s=%s" % (k, v) \
                    for k, v in params.iteritems())
            request = urllib2.Request(url + "?" + encoded_params, headers=headers)
            response = urllib2.urlopen(request)
            return Response(response.read(), response.headers)

try:
    from objectifier import Objectifier
except ImportError:
    Objectifier = lambda k: k

import settings

PARAMS = lambda: {
    'oauth_nonce': str(uuid.uuid4()),
    'oauth_timestamp': str(int(time.time())),
    'oauth_consumer_key': settings.KEY,
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_version': '1.0'
}

encode_tuple = lambda k, v: urllib.quote(k) + '%3D' + urllib.quote(urllib.quote(v, safe=''))

def generate_base_string(method, url, params):
    """
    Generate a base string using the given method, url, and URL parameters.
    """
    sorted_params = sorted(params.iteritems(), key=itemgetter(0))
    encoded_params = '%26'.join([encode_tuple(k, v) for k, v in sorted_params])
    return '&'.join([method, urllib.quote_plus(url), encoded_params])

def generate_signature(base_string, oauth_token_secret=None):
    """
    Generate an HMAC signature with the given base string and the
    ``oauth_token_secret``, if provided.
    """
    signing_key = settings.SECRET + '&'
    if oauth_token_secret:
        signing_key += oauth_token_secret

    hash = hmac.new(signing_key, base_string, hashlib.sha1)
    return hash.digest().encode('base-64')[:-1]


class TwitterError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class TwitterCall(object):
    """
    Helper class that performs all the work behind the scenes for the
    ``Twitter`` object.
    """
    def __init__(self, token, secret, endpoint_components):
        self.token = token
        self.secret = secret
        self.endpoint_components = endpoint_components
        self.base = settings.INSECURE_URL

    def __getattr__(self, k):
        self.endpoint_components.append(k)
        return self.__class__(self.token, self.secret, self.endpoint_components)

    def __getitem__(self, k):
        self.endpoint_components.append(str(k))
        return self.__class__(self.token, self.secret, self.endpoint_components)

    def __call__(self, method='GET', **kwargs):
        resource = "/".join(self.endpoint_components)
        if 'oauth_verifier' in kwargs or 'oauth_callback' in kwargs:
            url = "{}{}".format(self.base, resource)
        else:
            url = "{}1/{}.json".format(self.base, resource)

        signing_params = PARAMS()
        signing_params.update(kwargs)

        if self.token:
            signing_params['oauth_token'] = self.token

        base_string = generate_base_string(method, url, signing_params)

        header_params = {}
        query_params = {}
        for key, value in signing_params.iteritems():
            if key.startswith("oauth_"):
                header_params[key] = urllib.quote(value, safe='')
            else:
                query_params[key] = urllib.quote(value)

        signature = generate_signature(base_string, self.secret)
        header_params['oauth_signature'] = urllib.quote_plus(signature)
        headers = {'Authorization': 'OAuth realm="", %s' % ', '.join(['%s="%s"' % (k, v)
            for k, v in header_params.iteritems()])}

        kwargs = {'headers': headers}
        if method == 'POST':
            request_method = requests.post
            kwargs['data'] = query_params
        else:
            request_method = requests.get
            kwargs['params'] = query_params

        response = request_method(url, **kwargs)
        if 'text/html' in response.headers['content-type']:
            return Objectifier(urlparse.parse_qsl(response.text))

        response = Objectifier(response.text)

        if 'error' in response:
            raise TwitterError(response.error)

        return response

class SecureTwitterCall(TwitterCall):
    """
    A subclass of TwitterCall that performs all requests over SSL.
    """
    def __init__(self, *args, **kwargs):
        super(SecureTwitterCall, self).__init__(*args, **kwargs)
        self.base = settings.BASE_URL


class Twitter():
    """
    Exposes a simple mechanism to interact with the Twitter API. E.g.,

    >>> twitter = Twitter(access_token, access_secret_secret)
    >>> twitter.favorites()
    >>> twitter.statuses.user_timeline()
    >>> twitter.statuses.user_timeline(screen_name='elmcitylabs')
    """
    def __init__(self, token=None, secret=None, ssl=True):
        self.token = token
        self.secret = secret
        self.callee = SecureTwitterCall if ssl else TwitterCall

    def __getitem__(self, k):
        return self.callee(self.token, self.secret, [k])

    def __getattr__(self, k):
        return self.callee(self.token, self.secret, [k])

    def generate_authorization(self, callback=None):
        if callback:
            params = {'oauth_callback': callback}
        else:
            params = {'oauth_callback': settings.REDIRECT_URL}

        response = self.oauth.request_token(**params)
        url = "{}oauth/authorize?oauth_token={}".format(settings.BASE_URL, \
                response.oauth_token)
        return url, response.oauth_token, response.oauth_token_secret

    def __dir__(self):
        return ["generate_authorization"]

