"""Tests for tcn.apps.sitemaps.views"""

from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status

from tcn.apps.sitemaps.views import sitemaps


# Create your tests here.
class SitemapViewTests(TestCase):
    """Sitemap view tests"""

    def test_sitemap_index(self) -> None:
        """Test sitemaps"""

        response = self.client.get(reverse_lazy("django.contrib.sitemaps.views.index"))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Sitemap index failed with status code: {response.status_code}.",
        )

    def test_sitemap_section(self) -> None:
        """Test sitemaps"""

        for section in sitemaps.keys():
            response = self.client.get(
                reverse_lazy("django.contrib.sitemaps.views.sitemap", args=[section])
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
                f"Sitemap section {section} failed with status code: {response.status_code}.",
            )
