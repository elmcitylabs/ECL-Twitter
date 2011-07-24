from django.dispatch import Signal

post_twitter_auth = Signal(providing_args=['data'])

