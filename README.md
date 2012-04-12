How to get started
==================

1. Run `pip install ecl_twitter`.

2. In your `settings.py` file, insert the following three constants:

        TWITTER_KEY = "Gmxb5Rh7gpOpzunQ7SQcOA"
        TWITTER_SECRET = "irhZg1W5NO2r7M9IRwhjHKpzKPjJ3HXc6RYCbrM0"
        TWITTER_REDIRECT_URL = "http://example.com/oauth/complete"

    Or, alternatively, set the key, secret, and redirect URL in your environment.

        export TWITTER_KEY="Gmxb5Rh7gpOpzunQ7SQcOA"
        export TWITTER_SECRET="irhZg1W5NO2r7M9IRwhjHKpzKPjJ3HXc6RYCbrM0"
        export TWITTER_REDIRECT_URL="http://example.com/oauth/complete"

3. In your `views.py`, define a view to handle the callback.

        from ecl_twitter.decorators import twitter_callback

        @twitter_callback
        def oauth_twitter_complete(request, data):
            # XXX custom code
            # `data` is a dictionary containing
            # * oauth_token_secret
            # * oauth_token
            # * user_id
            # * screen_name
            # Do what you need to do with this data.


3. In your `urls.py`, add the following url patterns.

        url(r'^oauth/twitter/complete', 'views.oauth_twitter_complete',
            name='oauth-twitter-complete'),
        url(r'^oauth/twitter/', include('ecl_twitter.urls')),

4. You're done. Twitter is integrated with your application!

