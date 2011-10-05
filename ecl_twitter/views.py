import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET

import twitter

from decorators import twitter_callback

logger = logging.getLogger(__name__)

@require_GET
def twitter_oauth_begin(request):
    client = twitter.Twitter()
    data = client.generate_authorization_url()
    token = data['oauth_token']
    secret = data['oauth_token_secret']

    request.session['temporary_oauth_token'] = token
    request.session['temporary_oauth_secret'] = secret
    url = twitter.TWITTER_BASE_URL + twitter.TWITTER_OAUTH_AUTHORIZE
    return HttpResponseRedirect(url + '?oauth_token=' + token)

@require_GET
@twitter_callback
def twitter_oauth_complete(request, data):
    return HttpResponseRedirect(settings.TWITTER_REDIRECT_URL)

