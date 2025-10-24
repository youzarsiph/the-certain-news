"""Test view responses for GET methods"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status

from tcn import APP_NAME
from tcn.ui.tests import USERS

User = get_user_model()


# Create your tests here.
class ViewTests(TestCase):
    """View tests"""

    urlpatterns = {
        "login_required": {
            "profile": [],
        },
        "public": {
            "atom-latest": [],
            "atom-breaking": [],
            "rss-latest": [],
            "rss-breaking": [],
            "author": [USERS["user"]["slug"]],
            "authors": [],
            "search": [],
            "articles": [],
            "following-articles": [],
            "saved-articles": [],
            "archive": [],
            "articles-y": [2025],
            "articles-m": [2025, 1],
            "articles-d": [2025, 1, 1],
            # The following 2 test require the existence of an article
            # "article": [2025, 1, 1, "slug"],
            # "redirect": ["slug"],
        },
    }

    @classmethod
    def setUpTestData(cls) -> None:
        """Setup data"""

        cls.user = User.objects.create_user(**USERS["user"])

    def test_public_views(self) -> None:
        """Test public views"""

        for url, args in self.urlpatterns["public"].items():
            response = self.client.get(reverse_lazy(f"{APP_NAME}:{url}", args=args))
            self.assertIn(
                response.status_code,
                [status.HTTP_200_OK, status.HTTP_302_FOUND],
                f"Failed for {url}",
            )

    def test_login_required_views(self) -> None:
        """Test login required views"""

        # Authenticate user
        self.client.login(
            username=USERS["user"]["username"],
            password=USERS["user"]["password"],
        )

        for url, args in self.urlpatterns["login_required"].items():
            response = self.client.get(reverse_lazy(f"{APP_NAME}:{url}", args=args))
            self.assertIn(
                response.status_code,
                [status.HTTP_200_OK, status.HTTP_302_FOUND],
                f"Failed for {url}: {response.status_code}",
            )
