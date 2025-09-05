"""Feeds views"""

from tcn.apps.feeds.base import BaseArticleAtomFeed, BaseArticleFeed


# Create your views here.
class LatestNewsFeed(BaseArticleFeed):
    """Latest news feed"""

    link = "/feeds/rss/"

    def items(self):
        return super().items().order_by("-created_at")[:25]


class ArticlesAtomFeed(BaseArticleAtomFeed, LatestNewsFeed):
    """Atom Latest news feed"""

    link = "/feeds/atom/"


class BreakingNewsFeed(BaseArticleFeed):
    """Breaking news feed"""

    link = "/feeds/breaking/rss/"

    def items(self):
        return super().items().filter(is_breaking=True).order_by("-created_at")[:25]


class BreakingNewsAtomFeed(BaseArticleAtomFeed, BreakingNewsFeed):
    """Breaking news feed"""

    link = "/feeds/breaking/atom/"
