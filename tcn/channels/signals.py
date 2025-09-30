"""Signals to send breaking news to live feed"""

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.urls import reverse_lazy
from django.utils.timesince import timesince
from wagtail.signals import page_published

from tcn.apps.articles.models import Article


# Create your signals here.
def send_to_live_feed(sender, **kwargs):
    """Send breaking news to live feed"""

    channel_layer = get_channel_layer()

    if not channel_layer:
        return

    article: Article = kwargs["instance"]

    if article.is_breaking:
        async_to_sync(channel_layer.group_send)(
            f"{article.locale.language_code}-live",
            {
                "type": "broadcast",
                "article": {
                    "url": str(reverse_lazy("ui:redirect", args=[article.link.slug])),
                    "title": article.title,
                    "created_at": timesince(article.created_at),
                },
            },
        )


def register_live_feed():
    """Register the signal"""

    page_published.connect(send_to_live_feed, sender=Article)
