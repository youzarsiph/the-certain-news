"""Base classes for reuse"""

from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils.feedgenerator import Atom1Feed
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _

from tcn.apps.articles.models import Article


# Create your views here.
class BaseArticleFeed(Feed):
    """Base class for RSS feeds"""

    title = _("The Certain News feed")
    author_name = _("The Certain News")
    author_email = "feed@certain.news"
    description = _("Latest new from the World")

    def items(self):
        return (
            Article.objects.live()
            .public()
            .prefetch_related("link")
            .filter(locale__language_code=get_language())
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.headline

    def item_pubdate(self, item):
        return item.created_at

    def item_updateddate(self, item):
        return item.updated_at

    def item_categories(self, item):
        return [item.get_parent().title]

    def item_link(self, item):
        return reverse_lazy("ui:redirect", args=[item.link.slug])


class BaseArticleAtomFeed(BaseArticleFeed):
    """Base class for Atom feeds"""

    feed_type = Atom1Feed
    subtitle = BaseArticleFeed.description
