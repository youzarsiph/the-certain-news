"""Feeds views"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy
from wagtail.contrib.sitemaps.sitemap_generator import Sitemap as WagtailSitemap

from tcn import APP_NAME


# Create your views here
class StaticSitemap(Sitemap):
    """Static views sitemap"""

    i18n = True
    priority = 0.5
    alternates = True
    changefreq = "monthly"

    def items(self):
        return [
            "login",
            "logout",
            "subscribe",
            "profile",
            "following",
            "password_change",
            "password_reset",
            "atom-latest",
            "atom-breaking",
            "rss-latest",
            "rss-breaking",
            "following-articles",
            "saved-articles",
            "archive",
        ]

    def location(self, item):
        return reverse_lazy(f"{APP_NAME}:{item}")


sitemaps = {
    "static": StaticSitemap,
    "cms": WagtailSitemap,
}
