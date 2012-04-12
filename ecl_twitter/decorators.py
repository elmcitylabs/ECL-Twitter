from functools import wraps
import logging

import twitter
from signals import post_twitter_auth

logger = logging.getLogger(__name__)

def twitter_begin(fun):
    @wraps(fun)
    def inner(request, *args, **kwargs):
        fun(request, *args, **kwargs)
        client = twitter.Twitter()
        url, token, secret = client.generate_authorization()
        request.session['temporary_oauth_token'] = token
        request.session['temporary_oauth_secret'] = secret
        return HttpResponseRedirect(url)
    return inner

def twitter_callback(fun):
    @wraps(fun)
    def inner(request, *args, **kwargs):
        token = request.GET.get('oauth_token')
        verifier = request.GET.get('oauth_verifier')

        if token is None or verifier is None:
            raise Exception("Either `token` or `verifier` must be present in the callback URL.")

        if token != request.session['temporary_oauth_token']:
            raise Exception("tokens don't match, do not move forward with authentication")

        secret = request.session['temporary_oauth_secret']
        client = twitter.Twitter(token, secret)
        data = client.oauth.access_token(oauth_verifier=verifier)
        post_twitter_auth.send('ecl_twitter', data=data)
        return fun(request, data, *args, **kwargs)
    return inner


