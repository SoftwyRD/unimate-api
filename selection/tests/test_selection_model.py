from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Selection

PAYLOAD = {
    "name": "Test Subject",
}


def create_selection():
    selection = Selection.objects.create(**PAYLOAD)
    return selection


def create_user():
    defauls = {
        "first_name": "Test",
        "last_name": "User",
        "username": "test.user",
        "email": "test.user@example.com",
        "password": "testpass123",
    }
    user = get_user_model().objects.create(**defauls)
    return user


class TestSubjectModel(TestCase):
    def setUp(self):
        user = create_user()
        PAYLOAD.update({"user": user})

    def test_create_selection_success(self):
        """Test creating a selection"""

        selection = create_selection()

        self.assertEqual(selection.name, PAYLOAD["name"])
        self.assertEqual(selection.user, PAYLOAD["user"])

    def test_partial_update_selection(self):
        """Test updating a selection"""

        selection = create_selection()
        new_name = "Another selection"
        Selection.objects.update(name=new_name)
        selection.refresh_from_db()

        self.assertEqual(selection.name, new_name)
        self.assertEqual(selection.user, PAYLOAD["user"])

    def test_delete_selection(self):
        """Test deleting a selection"""

        selection = create_selection()
        selection.delete()
        selection = Selection.objects.filter(name=PAYLOAD["name"])

        self.assertFalse(selection.exists())

    def test_get_selection(self):
        """Test getting a selection"""

        create_selection()
        selection = Selection.objects.filter(name=PAYLOAD["name"])

        self.assertTrue(selection.exists())

    def test_get_all_selections(self):
        """Test getting all selections"""

        create_selection()
        create_selection()

        selections = Selection.objects.all()

        self.assertEqual(selections.count(), 2)
