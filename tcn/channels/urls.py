"""URL Configuration for tcn.channels"""

from django.urls import re_path

from tcn.channels.consumers import LiveFeedConsumer

# Create your URLConf here.
urlpatterns = [
    re_path(r"ws/live-feed/$", LiveFeedConsumer.as_asgi()),
]
