from django.contrib.auth import get_user_model
from django.test import TestCase

from selection.models import Selection

from ..models import Subject, SubjectSection

PAYLOAD = {
    "section": 3,
    "professor": "Samuel",
    "taken": False,
}


def create_selection_section(**params):
    return SubjectSection.objects.create(**params)


def create_user(**kwargs):
    defauls = {
        "first_name": "Test",
        "last_name": "User",
        "username": "test.user",
        "email": "test.user@example.com",
        "password": "testpassword123",
    }
    defauls.update(**kwargs)
    return get_user_model().objects.create(**defauls)


def create_selection(**kwargs):
    defaults = {
        "name": "My Selection",
    }
    defaults.update(**kwargs)
    return Selection.objects.create(**defaults)


def create_subject(**kwargs):
    defaults = {
        "code": "TST101",
        "name": "Test Subject",
        "credits": 2,
        "is_lab": False,
    }
    defaults.update(**kwargs)
    return Subject.objects.create(**defaults)


class TestSelectionSectionModel(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name="Test",
            last_name="User",
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
        self.selection = Selection.objects.create(
            name="My Selection",
            user=self.user,
        )
        self.subject = Subject.objects.create(
            code="TST101",
            name="Test Subject",
            credits=2,
            is_lab=False,
        )
        PAYLOAD.update(
            {
                "selection": self.selection,
                "subject": self.subject,
            }
        )

    def test_create_selection_section_success(self):
        """Test creating a selection section"""

        selection_section = create_selection_section(**PAYLOAD)

        self.assertEqual(selection_section.selection, PAYLOAD["selection"])
        self.assertEqual(selection_section.section, PAYLOAD["section"])
        self.assertEqual(selection_section.subject, PAYLOAD["subject"])
        self.assertEqual(selection_section.professor, PAYLOAD["professor"])
        self.assertEqual(selection_section.taken, PAYLOAD["taken"])

    def test_partial_update_selection_section(self):
        """Test updating a selection section"""

        new_professor = "Michael"
        selection_section = create_selection_section(**PAYLOAD)
        SubjectSection.objects.update(professor=new_professor)
        selection_section.refresh_from_db()

        self.assertEqual(selection_section.selection, PAYLOAD["selection"])
        self.assertEqual(selection_section.section, PAYLOAD["section"])
        self.assertEqual(selection_section.subject, PAYLOAD["subject"])
        self.assertEqual(selection_section.professor, new_professor)
        self.assertEqual(selection_section.taken, PAYLOAD["taken"])

    def test_delete_selection_section(self):
        """Test deleting a selection section"""

        selection_section = create_selection_section(**PAYLOAD)
        selection_section.delete()
        selection_section = SubjectSection.objects.filter(
            professor=PAYLOAD["professor"]
        )

        self.assertFalse(selection_section)

    def test_get_selection_section(self):
        """Test getting a selection section"""

        create_selection_section(**PAYLOAD)
        selection_section = SubjectSection.objects.get(
            professor=PAYLOAD["professor"]
        )

        self.assertTrue(selection_section)

    def test_get_all_selection_sections(self):
        """Test getting all selection sections"""

        create_selection_section(**PAYLOAD)

        PAYLOAD.update(
            {
                "section": 1,
                "professor": "Michael",
                "taken": True,
                "subject": self.subject,
                "selection": self.selection,
            }
        )
        create_selection_section(**PAYLOAD)

        selection_sections = SubjectSection.objects.all()

        self.assertEqual(selection_sections.count(), 2)
