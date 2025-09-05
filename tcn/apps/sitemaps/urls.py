"""Feeds URLConf"""

from django.urls import path
from wagtail.contrib.sitemaps import views

from tcn.apps.sitemaps.views import sitemaps

# Create your URLConf here.
urlpatterns = [
    path(
        "sitemap.xml",
        views.index,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.index",
    ),
    path(
        "sitemap-<section>.xml",
        views.sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]
