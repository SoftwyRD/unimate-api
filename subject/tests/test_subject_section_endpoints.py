from django.contrib.auth import get_user_model

# from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from college.models import CollegeModel
from selection.models import SelectionModel

from ..models import SubjectModel, SubjectSectionModel, SelectedSectionModel


def subject_section_url(id):
    return reverse("subject:sections", args=[id])


def create_user(**kwargs):
    defaults = {
        "first_name": "first_name",
        "last_name": "last_name",
        "email": "email@example.com",
        "username": "username",
        "password": "password123",
    }
    defaults.update(**kwargs)
    return get_user_model().objects.create(**defaults)


def create_selection(**kwargs):
    defaults = {
        "name": "My Selection",
    }
    defaults.update(**kwargs)
    return SelectionModel.objects.create(**defaults)


def create_subject(**kwargs):
    defaults = {
        "code": "TST101",
        "name": "Test Subject",
        "credits": 2,
        "is_lab": False,
    }
    defaults.update(**kwargs)
    return SubjectModel.objects.create(**defaults)


def create_subject_section(selection, subject, **kwargs):
    defaults = {
        "section": 1,
        "professor": "Marco Antonio",
    }
    defaults.update(subject=subject, **kwargs)
    section = SubjectSectionModel.objects.create(**defaults)
    SelectedSectionModel.objects.create(selection=selection, section=section)
    return section


class TestSubjectSectionEndpoints(APITestCase):
    def setUp(self):
        self.client = APIClient()

        user = create_user()
        self.client.force_authenticate(user=user)

        college = CollegeModel.objects.create(name="test", full_name="Test")

        self.subject = create_subject(college=college)
        self.selection = create_selection(owner=user)
        self.subject_section = create_subject_section(
            self.selection, self.subject
        )

        self.payload = self.subject_section.__dict__

    # def test_retireve_subject_sections(self):
    #     """Test that the subject sections can be retrieved"""

    #     response = self.client.get(
    #         reverse("selection:subjects", args=[self.selection.id])
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn("next", response.data)
    #     self.assertIn("previous", response.data)
    #     self.assertIn("results", response.data)
    #     self.assertIn("count", response.data)

    # def test_create_subject_section(self):
    #     """Test that the subject section can be created"""

    #     response = self.client.post(
    #         reverse("selection:subjects", args=[self.selection.id]),
    #         self.payload,
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_update_subject_section(self):
    #     """Test that the subject section can be updated"""

    #     response = self.client.patch(
    #         subject_section_url(self.subject_section.id),
    #         self.payload,
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_delete_subject_section(self):
    #     """Test that the subject section can be deleted"""

    #     response = self.client.delete(
    #         subject_section_url(self.subject_section.id)
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(response.data, None)
