from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

LOGIN_URL = reverse("security:pair-token")
LOGIN_REFRESH_URL = reverse("security:refresh-token")
SIGN_UP_URL = reverse("security:sign-up")
PROFILE_URL = reverse("user:profile")


class TestPublicUserEndpoints(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.PAYLOAD = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        }

        user = get_user_model().objects.create(**self.PAYLOAD)
        self.client.force_authenticate(user)

    def test_register_user_success(self):
        """Test registering a new user is successful"""

        PAYLOAD = {
            "first_name": "User",
            "last_name": "Test",
            "username": "usertest",
            "email": "usertest@example.com",
            "password": "passtest123",
        }
        response = self.client.post(SIGN_UP_URL, PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response["Location"], PROFILE_URL)

        self.assertNotIn("password", response.data)
        self.assertEqual(response.data["username"], PAYLOAD["username"])

    def test_login_success(self):
        """Test logging in a user is successful"""

        PAYLOAD = {
            "username": self.PAYLOAD["username"],
            "password": self.PAYLOAD["password"],
        }

        response = self.client.post(LOGIN_URL, PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_not_registered(self):
        """Test logging in a user that is not registered"""

        PAYLOAD = {
            "username": "not_an_valid_user",
            "password": "not_a_valid_password",
        }

        response = self.client.post(LOGIN_URL, PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
