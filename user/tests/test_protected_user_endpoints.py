from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

LOGIN_URL = reverse("security:access-token")
LOGIN_REFRESH_URL = reverse("security:refresh-token")
PROFILE_URL = reverse("user:profile")


class TestProtectedUserEndpoints(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.PAYLOAD = {
            "first_name": "Test",
            "last_name": "User",
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        self.user = get_user_model().objects.create(**self.PAYLOAD)
        self.client.force_authenticate(self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""

        response = self.client.get(PROFILE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

        self.assertNotIn("password", response.data)

    def test_update_profile_success(self):
        """Test updating the user profile for authenticated user"""

        PAYLOAD = {
            "email": "anothermail@example.com",
        }

        response = self.client.patch(PROFILE_URL, PAYLOAD)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["email"], PAYLOAD["email"])
