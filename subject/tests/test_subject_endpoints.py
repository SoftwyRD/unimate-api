from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ..models import SubjectModel


def list_url():
    return reverse("subject:list")


def detail_url(id):
    return reverse("subject:detail", args=[id])


def create_subject(**kwargs):
    defaults = {
        "code": "TST101",
        "name": "Test Subject",
        "credits": 1,
        "is_lab": 0,
    }
    defaults.update(**kwargs)
    return SubjectModel.objects.create(**defaults)


class TestSubjectEndpoints(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.subject = create_subject()

    def test_list_subjects_success(self):
        """Test that unauthenticated user can list subjects"""

        response = self.client.get(list_url())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_get_subject_success(self):
        """Test that unauthenticated user can get subjects"""

        response = self.client.get(detail_url(self.subject.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
