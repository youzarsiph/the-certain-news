"""Tests for tcn.api.viewsets.UserViewSet"""

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


# Create your tests here.
class UserViewSetTests(APITestCase):
    """UserViewSet tests"""

    users = {
        "follower": {
            "username": "follower",
            "email": "follower@tests.com",
            "password": "follower.tests.1234",
            "slug": "follower",
        },
        "writer": {
            "username": "writer",
            "email": "writer@tests.com",
            "password": "writer.tests.1234",
            "slug": "writer",
        },
    }

    @classmethod
    def setUpTestData(cls) -> None:
        """Setup data"""

        cls.writer = User.objects.create_user(**cls.users["writer"])
        cls.follower = User.objects.create_user(**cls.users["follower"])

    def test_follow_user_action(self) -> None:
        """Test `follow` extra action in UserViewSet"""

        # Authenticate
        self.client.login(
            username=self.users["follower"]["username"],
            password=self.users["follower"]["password"],
        )

        # Follow writer
        response = self.client.post(
            reverse_lazy("user-follow", args=[self.users["writer"]["slug"]]),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, "Failed to follow")
        self.assertEqual(
            response.data.get("detail", None),
            _(f"You are following {self.users['writer']['username']}."),
            "Follow detail message did not match.",
        )

        # Unfollow writer
        response = self.client.post(
            reverse_lazy("user-follow", args=[self.users["writer"]["slug"]]),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, "Failed to unfollow")
        self.assertEqual(
            response.data.get("detail", None),
            _(f"You are no longer following {self.users['writer']['username']}."),
            "Unfollow detail message did not match.",
        )
