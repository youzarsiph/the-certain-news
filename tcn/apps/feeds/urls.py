"""Feeds URLConf"""

from django.urls import path

from tcn.apps.feeds import views

# Create your URLConf here.
urlpatterns = [
    path("rss/", views.LatestNewsFeed(), name="rss-latest"),
    path("atom/", views.ArticlesAtomFeed(), name="atom-latest"),
    path("breaking/rss/", views.BreakingNewsFeed(), name="rss-breaking"),
    path("breaking/atom/", views.BreakingNewsAtomFeed(), name="atom-breaking"),
]
