import uuid

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

SELECTION_LIST_URL = reverse("selection:list")

PAYLOAD = {
    "name": "name",
}


def selection_detail_url(id):
    return reverse("selection:detail", args=[str(id)])


def create_user(**kwargs):
    defauls = {
        "first_name": "Test",
        "last_name": "User",
        "username": "test.user",
        "email": "test.user@example.com",
        "password": "testpass123",
    }
    defauls.update(**kwargs)
    user = get_user_model().objects.create(**defauls)
    return user


class PublicSelectionAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_post_selection(self):
        """Test post selection"""

        res = self.client.post(SELECTION_LIST_URL, PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_selections(self):
        """Test get selections"""

        res = self.client.get(SELECTION_LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_selection(self):
        """Test get selection"""

        res = self.client.get(selection_detail_url(uuid.uuid1()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_selection(self):
        """Test delete selection"""

        res = self.client.delete(selection_detail_url(uuid.uuid1()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_selection(self):
        """Test patch selection"""

        res = self.client.patch(selection_detail_url(uuid.uuid1()))
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
