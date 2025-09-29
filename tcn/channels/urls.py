"""URL Configuration for tcn.channels"""

from django.urls import path

from tcn.channels.consumers import LiveFeedConsumer

# Create your URLConf here.
app_name = "tcn_live"

urlpatterns = [
    path("wss/<slug:language_code>/live/", LiveFeedConsumer.as_asgi(), name="live"),
]
