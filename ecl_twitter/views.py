import logging

from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_GET

import twitter

from decorators import twitter_callback

logger = logging.getLogger(__name__)

@require_GET
def oauth_twitter_begin(request):
    client = twitter.Twitter()
    url, token, secret = client.generate_authorization()
    request.session['temporary_oauth_token'] = token
    request.session['temporary_oauth_secret'] = secret
    return HttpResponseRedirect(url)

@require_GET
@twitter_callback
def oauth_twitter_complete(request, data):
    return HttpResponseRedirect(settings.TWITTER_REDIRECT_URL)

