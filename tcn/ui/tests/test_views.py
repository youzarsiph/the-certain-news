"""Tests for tcn.ui.views"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status

User = get_user_model()


# Create your tests here.
class ViewTests(TestCase):
    """View tests"""

    user_info = {
        "username": "user",
        "email": "user@tests.com",
        "password": "user.tests.1234",
        "slug": "user",
    }
    urlpatterns = {
        "login_required": {
            "profile": [],
            "u-user": [user_info["slug"]],
            "d-user": [user_info["slug"]],
            "password_change": [],
            "password_change_done": [],
            "password_reset_confirm": ["uidb64", "token"],
        },
        "public": {
            "password_reset": [],
            "password_reset_done": [],
            "password_reset_complete": [],
            "login": [],
            "subscribe": [],
            "atom-latest": [],
            "atom-breaking": [],
            "rss-latest": [],
            "rss-breaking": [],
            "author": [user_info["slug"]],
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

        cls.user = User.objects.create_user(**cls.user_info)

    def test_public_views(self) -> None:
        """Test public views"""

        for url, args in self.urlpatterns["public"].items():
            response = self.client.get(reverse_lazy(f"tcn:{url}", args=args))
            self.assertIn(
                response.status_code,
                [status.HTTP_200_OK, status.HTTP_302_FOUND],
                f"Failed for {url}",
            )

    def test_login_required_views(self) -> None:
        """Test login required views"""

        # Authenticate user
        self.client.login(
            username=self.user_info["username"],
            password=self.user_info["password"],
        )

        for url, args in self.urlpatterns["login_required"].items():
            response = self.client.get(reverse_lazy(f"tcn:{url}", args=args))
            self.assertIn(
                response.status_code,
                [status.HTTP_200_OK, status.HTTP_302_FOUND],
                f"Failed for {url}",
            )
