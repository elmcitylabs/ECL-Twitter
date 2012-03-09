from functools import wraps

import twitter
import logging
from django.http import HttpResponseRedirect
from signals import post_twitter_auth

logger = logging.getLogger(__name__)

def twitter_begin(fun):
    @wraps(fun)
    def k(request, *args, **kwargs):
        client = twitter.Twitter()
        data = client.generate_authorization_url()
        token = data['oauth_token']
        secret = data['oauth_token_secret']

        request.session['temporary_oauth_token'] = token
        request.session['temporary_oauth_secret'] = secret
        url = twitter.TWITTER_BASE_URL + twitter.TWITTER_OAUTH_AUTHORIZE
        return HttpResponseRedirect(url + '?oauth_token=' + token)

    return k

def twitter_callback(fun):
    def k(request, *args, **kwargs):
        token = request.GET['oauth_token']
        verifier = request.GET['oauth_verifier']

        if token != request.session['temporary_oauth_token']:
            logger.warning("tokens don't match, do not move forward with authentication")

        secret = request.session['temporary_oauth_secret']
        client = twitter.Twitter(token, secret)
        data = client.generate_access_token(verifier)

        post_twitter_auth.send('ecl_twitter', data=data)
        return fun(request, data, *args, **kwargs)
    return k


