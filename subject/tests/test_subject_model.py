from django.test import TestCase

from ..models import Subject

PAYLOAD = {
    "code": "TST101",
    "name": "Test Subject",
    "credits": 3,
    "is_lab": False,
}


def create_subject(**params):
    """Helper function to create a subject"""
    subject = Subject.objects.create(**params)
    return subject


class SubjectModelTests(TestCase):
    """Test subject model"""

    def test_create_subject_success(self):
        """Test creating a subject"""

        subject = create_subject(**PAYLOAD)

        self.assertEqual(subject.code, PAYLOAD["code"])
        self.assertEqual(subject.name, PAYLOAD["name"])
        self.assertEqual(subject.credits, PAYLOAD["credits"])
        self.assertEqual(subject.is_lab, PAYLOAD["is_lab"])

    def test_partial_update_subject(self):
        """Test updating a subject"""

        new_credits = 4
        subject = create_subject(**PAYLOAD)
        Subject.objects.update(credits=new_credits)
        subject.refresh_from_db()

        self.assertEqual(subject.code, PAYLOAD["code"])
        self.assertEqual(subject.name, PAYLOAD["name"])
        self.assertEqual(subject.credits, new_credits)
        self.assertEqual(subject.is_lab, PAYLOAD["is_lab"])

    def test_delete_subject(self):
        """Test deleting a subject"""

        subject = create_subject(**PAYLOAD)
        subject.delete()
        subject = Subject.objects.filter(credits=PAYLOAD["credits"])

        self.assertFalse(subject)

    def test_get_subject(self):
        """Test getting a subject"""

        create_subject(**PAYLOAD)
        subject = Subject.objects.get(credits=PAYLOAD["credits"])

        self.assertTrue(subject)

    def test_get_all_subjects(self):
        """Test getting all subjects"""

        create_subject(**PAYLOAD)

        PAYLOAD.update(
            {
                "code": "TS5101L",
                "name": "Test Subject Laboratory",
                "credits": 4,
                "is_lab": True,
            }
        )
        create_subject(**PAYLOAD)

        subjects = Subject.objects.all()

        self.assertEqual(subjects.count(), 2)
