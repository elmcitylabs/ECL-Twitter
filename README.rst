ECL Twitter
===========

ECL Twitter is an awesome Twitter library for Python 2.7+. It makes the Twitter
API a joy to use, and Django integration is baked in. To find out more, read
on!

If you have an issue to report or a feature request, add it to our
`issue tracker <https://github.com/elmcitylabs/ECL-Twitter/issues>`_.

.. _installation:

Installation
------------

ECL Twitter is on PyPi, so we recommend installing via `pip`_::

    $ pip install ecl-twitter

.. _pip: http://www.pip-installer.org/en/latest/

.. _configuration:

Configuration
-------------

If you'd like to use ECL Twitter for a stand alone application (e.g., in a
script you're writing to download your tweets), you'll need to set the
environment variables ``TWITTER_KEY``, ``TWITTER_SECRET``, and
``TWITTER_REDIRECT_URL`` with the values appropriate for your Twitter
application.::

    export TWITTER_KEY="Gmxb5Rh7gpOpzunQ7SQcOA"
    export TWITTER_SECRET="irhZg1W5NO2r7M9IRwhjHKpzKPjJ3HXc6RYCbrM0"
    export TWITTER_REDIRECT_URL="http://example.com/oauth/complete"

If you're only interested in integration with Django, read `django`.

.. _authentication:

Authentication
--------------

We've made authentication very simple. Probably too simple, to be honest.::

    >>> from ecl_twitter import Twitter
    >>> twitter = Twitter()
    >>> url, token, secret = twitter.generate_authorization()
    >>> url
    https://api.twitter.com/oauth/authorize?oauth_token=XXX

After opening this URL in your browser and allowing the application, you'll be redirected to a page with a PIN. This is your ``verifier``.::

    >>> twitter = Twitter(token, secret)
    >>> data = twitter.oauth.access_token(oauth_verifier=verifier)
    >>> data
    <Objectifier#dict oauth_token_secret=unicode user_id=unicode oauth_token=unicode screen_name=unicode>

Congratulations, you have successfully authenticated with Twitter (told you it was easy). ``data`` is an ``Objectifier`` object which should contain your token, secret, user id, and screen name.

To call the API, use your newly-acquired access token and access token secret::

    >>> twitter = Twitter(data.oauth_token, data.oauth_token_secret)
    >>> tweets = twitter.statuses.user_timeline()
    >>> tweets
    <Objectifier#list elements:20>

So, yeah. That's it. Be fruitful and multiply.

.. _django:

Integrating with Django
-----------------------

What we did above is easy. For Django projects, we've made it even easier. In your views file::

    from django.contrib.auth import authenticate, login
    from django.http import HttpResponseRedirect

    from ecl_twitter import twitter_begin, twitter_callback

    from .models import User

    # ...

    @twitter_begin
    def oauth_twitter_begin(request):
        pass

    @twitter_callback
    def oauth_twitter_complete(request, data):
        user, _ = User.objects.get_or_create(screen_name=data.screen_name, defaults={
            'access_token': data.oauth_token,
            'access_token_secret': data.oauth_token_secret })
        user = authenticate(id=user.id)
        login(request, user)
        return HttpResponseRedirect(reverse('home'))

Add these values to your settings.::

    # The User model that you'll be using to authenticate with Twitter.
    PRIMARY_USER_MODEL = "app.User"

    AUTHENTICATION_BACKENDS = (
        # ...
        'ecl_twitter.backends.TwitterAuthBackend',
    )

    TWITTER_KEY = "Gmxb5Rh7gpOpzunQ7SQcOA"
    TWITTER_SECRET = "irhZg1W5NO2r7M9IRwhjHKpzKPjJ3HXc6RYCbrM0"
    TWITTER_REDIRECT_URL = "http://example.com/oauth/complete"

Then map the above views in your urls.py::

    # ...

    urlpatterns = patterns('app.views',
        # ...
        url(r'^oauth/twitter/begin$', 'oauth_twitter_begin'),
        url(r'^oauth/twitter/complete$', 'oauth_twitter_complete'),
    )

You're done. Oh, you might also want to add some fields for storing the
Twitter-related fields in your user model.

Contributing, feedback, and questions
-------------------------------------

* Github: https://github.com/elmcitylabs
* Bitbucket: http://bitbucket.com/elmcitylabs
* Email: opensource@elmcitylabs.com
* Twitter: `@elmcitylabs <http://twitter.com/elmcitylabs>`_

Indices and tables
==================

* `genindex`
* `modindex`
* `search`

