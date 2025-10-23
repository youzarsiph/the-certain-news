"""Tests for tcn.apps.feeds.views"""

from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status

from tcn import APP_NAME


# Create your tests here.
class FeedViewTests(TestCase):
    """Feed view tests"""

    urlpatterns = ["atom-latest", "atom-breaking", "rss-latest", "rss-breaking"]

    def test_news_feeds(self) -> None:
        """Test news feeds"""

        for pattern in self.urlpatterns:
            response = self.client.get(reverse_lazy(f"{APP_NAME}:{pattern}"))

            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
                f"Feed `{pattern}` failed with status code: {response.status_code}.",
            )
