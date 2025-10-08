"""Tests for tcn.api.viewsets.UserViewSet"""

from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


# Create your tests here.
class UserViewSetTests(APITestCase):
    """UserViewSet tests"""

    @classmethod
    def setUpTestData(cls) -> None:
        """Setup data"""

        cls.writer = User.objects.create_user(
            username="writer",
            email="wrtier@tests.com",
            password="writer.tests.1234",
            slug="writer",
        )
        cls.follower = User.objects.create_user(
            username="follower",
            email="follower@tests.com",
            password="follower.tests.1234",
            slug="follower",
        )

    def test_follow_user_action(self) -> None:
        """Test `follow` extra action in UserViewSet"""

        # Authenticate
        self.client.login(
            username=self.follower.username,
            password=f"{self.follower.username}.tests.1234",
        )

        # Follow writer
        response = self.client.post(
            reverse_lazy("user-follow", args=[self.writer.slug]),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, "Failed to follow")
        self.assertEqual(
            response.data.get("detail", None),
            _(f"You are following {self.writer.username}."),
            "Follow detail message did not match.",
        )

        # Unfollow writer
        response = self.client.post(
            reverse_lazy("user-follow", args=[self.writer.slug]),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, "Failed to unfollow")
        self.assertEqual(
            response.data.get("detail", None),
            _(f"You are no longer following {self.writer.username}."),
            "Unfollow detail message did not match.",
        )
