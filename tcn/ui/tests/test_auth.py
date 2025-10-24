"""Test auth system"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from rest_framework import status

from tcn import APP_NAME
from tcn.ui.tests import USERS

User = get_user_model()


# Create your tests here.
class AuthViewTests(TestCase):
    """Test authentication system"""

    @classmethod
    def setUpTestData(cls) -> None:
        """Setup data"""

        cls.user = User.objects.create_user(**USERS["writer"])

    def test_user_subscription(self) -> None:
        """Test user registration"""

        response = self.client.post(
            reverse_lazy(f"{APP_NAME}:subscribe"),
            {
                **USERS["user"],
                "first_name": "Test",
                "last_name": "User",
                "password1": USERS["user"]["password"],
                "password2": USERS["user"]["password"],
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"User subscription failed with status code: {response.status_code}.",
        )

    def test_login(self) -> None:
        """Test user login"""

        response = self.client.post(reverse_lazy(f"{APP_NAME}:login"), USERS["user"])

        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND,
            f"User login failed with status code: {response.status_code}.",
        )

    def test_profile(self) -> None:
        """Test user profile"""

        # Authenticate user
        self.client.login(
            username=USERS["writer"]["username"],
            password=USERS["writer"]["password"],
        )

        response = self.client.get(reverse_lazy(f"{APP_NAME}:profile"))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Profile view failed with status code: {response.status_code}.",
        )

    def test_logout(self) -> None:
        """Test user logout"""

        # Login
        self.client.login(
            username=USERS["user"]["username"],
            password=USERS["user"]["password"],
        )

        # Logout
        response = self.client.post(reverse_lazy(f"{APP_NAME}:logout"))

        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND,
            f"User logout failed with status code: {response.status_code}.",
        )

    def test_password_change(self) -> None:
        """Test user password change"""

        # Login
        self.client.login(
            username=USERS["user"]["username"],
            password=USERS["user"]["password"],
        )

        new_pass = USERS["user"]["password"] + "456789"

        # Logout
        response = self.client.post(
            reverse_lazy(f"{APP_NAME}:password_change"),
            {
                "old_password": USERS["user"]["password"],
                "new_password": new_pass,
                "new_password_confirm": new_pass,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_302_FOUND,
            f"User logout failed with status code: {response.status_code}.",
        )

        is_succeeded = self.client.login(
            username=USERS["user"]["username"],
            password=new_pass,
        )

        self.assertTrue(
            is_succeeded, "Password change failed: Unable to change password."
        )

    def test_user_update(self) -> None:
        """Test user update"""

        # Login
        self.client.login(
            username=USERS["writer"]["username"],
            password=USERS["writer"]["password"],
        )

        # Logout
        response = self.client.post(
            reverse_lazy(f"{APP_NAME}:u-user", args=[USERS["writer"]["slug"]]),
            {"first_name": "Updated"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"User update failed with status code: {response.status_code}.",
        )

        # Get updated user instance
        user = User.objects.get(slug=USERS["writer"]["slug"])

        self.assertEqual(
            user.first_name,
            "Updated",
            "User update failed: Unable to update `first_name` field.",
        )

    def test_user_delete(self) -> None:
        """Test user delete"""

        # Login
        self.client.login(
            username=USERS["writer"]["username"],
            password=USERS["writer"]["password"],
        )

        # Logout
        response = self.client.post(
            reverse_lazy(f"{APP_NAME}:d-user", args=[USERS["writer"]["slug"]])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            f"User update failed with status code: {response.status_code}.",
        )

        # Check if user is deleted
        self.assertQuerySetEqual(
            User.objects.filter(slug=USERS["writer"]["slug"]),
            [],
            msg="User delete failed: Unable to delete the user.",
        )
