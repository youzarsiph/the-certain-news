"""Signals to create page shortened links"""

from wagtail.signals import page_published, copy_for_translation_done

from tcn.apps.articles.models import Article
from tcn.apps.links.models import Link


def create_article_link(sender, **kwargs):
    """Create a new link for an article"""

    article = kwargs["instance"]
    _ = Link.objects.get_or_create(article=article)


def create_trans_article_link(sender, **kwargs):
    """Create a new link for translated article"""

    article = kwargs["target_obj"]
    _ = Link.objects.get_or_create(article=article)


def register_link_signal_receivers():
    """Register `create_article_link` and `create_trans_article_link` signals"""

    page_published.connect(create_article_link, sender=Article)
    copy_for_translation_done.connect(create_trans_article_link, sender=Article)
