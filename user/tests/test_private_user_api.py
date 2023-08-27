from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

LOGIN_URL = reverse("user:pair-token")
LOGIN_REFRESH_URL = reverse("user:refresh-token")
USER_LIST_URL = reverse("user:list")
ME_URL = reverse("user:me")


class TestPrivateUserAPI(APITestCase):
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

        res = self.client.get(ME_URL)
        data = res.data

        res_status = data["status"]
        res_data = data["data"]
        profile = res_data["profile"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn("status", data)
        self.assertEqual(res_status, "success")

        self.assertIn("data", data)
        self.assertIn("profile", res_data)

        self.assertIn("first_name", profile)
        self.assertIn("middle_name", profile)
        self.assertIn("last_name", profile)
        self.assertIn("username", profile)
        self.assertIn("email", profile)

        self.assertNotIn("password", profile)

    def test_update_profile_success(self):
        """Test updating the user profile for authenticated user"""

        PAYLOAD = {
            "email": "anothermail@example.com",
        }

        res = self.client.patch(ME_URL, PAYLOAD)
        user = get_user_model().objects.get(username=self.PAYLOAD["username"])

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(user.email, PAYLOAD["email"])
