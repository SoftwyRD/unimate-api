from django.test import TestCase
from core.models import Subject as SubjectModel
# from subject.serializers import SubjectSerializer
from rest_framework.reverse import reverse
# from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, force_authenticate
from rest_framework import status

SUBJECT_URL = reverse("subject:subject-list")


# Create your tests here.
class SubjectUnauthenticatedTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_subject_test_success(self) -> None:
        res = self.client.get(SUBJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_subject_test_success(self) -> None:

        subject = SubjectModel.objects.create(
            code='IDS222',
            name='Desarrollo de Software 1',
            credits=4,
            is_lab=0,
        )

        res = self.client.get(SUBJECT_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        # self.assertNotEqual(
        # subject.code, res.data["data"]["subjects"][0]['code'])
