"""Feeds views"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy
from wagtail.contrib.sitemaps.sitemap_generator import \
    Sitemap as WagtailSitemap


# Create your views here
class StaticSitemap(Sitemap):
    """Static views sitemap"""

    i18n = True
    priority = 0.5
    alternates = True
    changefreq = "daily"

    def items(self):
        return ["ui:search", "ui:articles", "ui:archive"]

    def location(self, item):
        return reverse_lazy(item)


sitemaps = {
    "static": StaticSitemap,
    "cms": WagtailSitemap,
}
