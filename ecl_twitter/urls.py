from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('ecl_twitter.views',
    url(r'begin$', 'oauth_twitter_begin', name='oauth-twitter-begin'),
)

