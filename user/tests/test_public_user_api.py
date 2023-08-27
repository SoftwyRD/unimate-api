from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

LOGIN_URL = reverse("user:pair-token")
LOGIN_REFRESH_URL = reverse("user:refresh-token")
USER_LIST_URL = reverse("user:list")
ME_URL = reverse("user:me")


def user_detail_url(user_id):
    return reverse("user:details", args=[user_id])


class TestPublicUserAPI(APITestCase):
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
        res = self.client.post(USER_LIST_URL, PAYLOAD)
        data = res.data

        res_status = data["status"]
        res_data = data["data"]
        user = res_data["user"]
        user_id = user["id"]

        user_location = user_detail_url(user_id)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res["Location"], user_location)

        self.assertIn("status", data)
        self.assertEqual(res_status, "success")

        self.assertIn("data", data)
        self.assertIn("user", res_data)

        self.assertNotIn("password", user)
        self.assertEqual(user["username"], PAYLOAD["username"])

    def test_login_success(self):
        """Test logging in a user is successful"""

        PAYLOAD = {
            "username": self.PAYLOAD["username"],
            "password": self.PAYLOAD["password"],
        }

        res = self.client.post(LOGIN_URL, PAYLOAD)
        data = res.data

        res_status = data["status"]
        res_data = data["data"]
        tokens = res_data["tokens"]

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertIn("status", data)
        self.assertEqual(res_status, "success")

        self.assertIn("data", data)
        self.assertIn("tokens", res_data)

        self.assertIn("access", tokens)
        self.assertIn("refresh", tokens)

    def test_login_not_registered(self):
        """Test logging in a user that is not registered"""

        PAYLOAD = {
            "username": "not_an_valid_user",
            "password": "not_a_valid_password",
        }

        res = self.client.post(LOGIN_URL, PAYLOAD)
        data = res.data

        res_status = data["status"]
        res_data = data["data"]

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        self.assertIn("status", data)
        self.assertEqual(res_status, "fail")

        self.assertIn("data", data)
        self.assertNotIn("tokens", res_data)
        self.assertIn("title", res_data)
        self.assertIn("message", res_data)
