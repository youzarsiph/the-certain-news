"""Feeds URLConf"""

from django.urls import path

from tcn.apps.feeds import views

# Create your URLConf here.
urlpatterns = [
    path("rss/", views.LatestNewsFeed()),
    path("atom/", views.ArticlesAtomFeed()),
    path("breaking/rss/", views.BreakingNewsFeed()),
    path("breaking/atom/", views.BreakingNewsAtomFeed()),
]
