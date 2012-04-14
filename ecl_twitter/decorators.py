from functools import wraps
import logging

from django.http import HttpResponseRedirect

import twitter

logger = logging.getLogger(__name__)

def twitter_begin(fun):
    """
    Django view decorator that gets a request token and secret from Twitter and
    redirects the user to a URL where they can authorize the application.
    """
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
    """
    Django view decorator that generates a Twitter OAuth access token and
    secret after the user authorizes the application. Must be used in
    conjunction with the ``twitter_begin`` decorator.

    The wrapped view is passed an ``Objectifier`` object containing the the
    access token, the access token secret, the user id, and the user's screen
    name.
    """
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

        from signals import post_twitter_auth
        post_twitter_auth.send('ecl_twitter', data=data)
        return fun(request, data, *args, **kwargs)
    return inner


