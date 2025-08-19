"""Signals to create page shortened links"""

from wagtail.signals import page_published

from tcn.apps.articles.models import Article
from tcn.apps.links.models import Link


def create_page_link(sender, **kwargs):
    """Create a new link for a page"""

    article = kwargs["instance"]
    _ = Link.objects.get_or_create(article=article)


def register_signal_receivers():
    """Register `create_page_link` signal"""

    page_published.connect(create_page_link, sender=Article)
