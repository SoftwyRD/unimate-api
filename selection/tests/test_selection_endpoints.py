from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from ..models import SelectionModel

SELECTION_LIST_URL = reverse("selection:list")

PAYLOAD = {
    "name": "My Selection",
}


def selection_detail_url(id):
    return reverse("selection:detail", args=[str(id)])


def create_user(**kwargs):
    defauls = {
        "first_name": "Test",
        "last_name": "User",
        "username": "test.user",
        "email": "test.user@example.com",
        "password": "testpassword123",
    }
    defauls.update(**kwargs)
    user = get_user_model().objects.create(**defauls)
    return user


def create_selection(**kwargs):
    defauls = PAYLOAD.copy()
    defauls.update(**kwargs)
    selection = SelectionModel.objects.create(**defauls)
    return selection


class TestSelectionEndpoints(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_list_selections_success(self):
        """Test list selections"""

        response = self.client.get(SELECTION_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)

    def test_post_selection(self):
        """Test post selection"""

        response = self.client.post(SELECTION_LIST_URL, PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], PAYLOAD["name"])
        self.assertIn("Location", response)

    def test_delete_selection(self):
        """Test delete selection"""

        selection = create_selection(user=self.user)
        response = self.client.delete(selection_detail_url(selection.id))

        selections = SelectionModel.objects.filter(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(selections.count(), 0)

    def test_delete_other_user_selection(self):
        """Test delete selection of other user should not be permited"""

        newUser = create_user(
            username="new.username",
            email="new.mail@example.com",
        )
        selection = create_selection(user=newUser)
        response = self.client.delete(selection_detail_url(selection.id))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_selection(self):
        """Test patch selection"""

        selection = create_selection(user=self.user)
        payload = {
            "name": "Best Selection",
        }
        response = self.client.patch(
            selection_detail_url(selection.id), payload
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], payload["name"])

    def test_patch_selection_of_other_user(self):
        """Test patch selection of other user should not be permited"""

        new_user = create_user(
            username="new.username",
            email="new.mail@example.com",
        )
        selection = create_selection(user=new_user)
        response = self.client.patch(
            selection_detail_url(selection.id), PAYLOAD
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
