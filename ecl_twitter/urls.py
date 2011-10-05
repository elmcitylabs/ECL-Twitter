from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('ecl_twitter.views',
    url(r'^begin$', 'twitter_oauth_begin', name='twitter-oauth-begin'),
)

