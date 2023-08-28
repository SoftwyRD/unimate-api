from django.contrib.auth import get_user_model
from django.test import TestCase

from selection.models import Selection

from ..models import SectionSchedule, Subject, SubjectSection, Weekday

PAYLOAD = {
    "start_time": 11,
    "end_time": 13,
}


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


def create_section(**kwargs):
    defaults = {
        "section": 2,
        "professor": "Michael",
        "taken": True,
    }
    defaults.update(**kwargs)
    return SubjectSection.objects.create(**defaults)


def create_weekday(**kwargs):
    defaults = {
        "name": "Monday",
    }
    defaults.update(**kwargs)
    return Weekday.objects.create(**defaults)


def create_schedule(**params):
    return SectionSchedule.objects.create(**params)


class TestScheduleModel(TestCase):
    def setUp(self):
        self.user = create_user()

        self.subject = create_subject()
        self.selection = create_selection(user=self.user)
        self.section = create_section(
            selection=self.selection, subject=self.subject
        )
        self.weekday = create_weekday()

        PAYLOAD.update(
            {
                "section": self.section,
                "weekday": self.weekday,
            }
        )

    def test_create_schedule_success(self):
        """Test that a schedule can be created"""

        schedule = create_schedule(**PAYLOAD)

        self.assertEqual(schedule.section, PAYLOAD["section"])
        self.assertEqual(schedule.weekday, PAYLOAD["weekday"])
        self.assertEqual(schedule.start_time, PAYLOAD["start_time"])
        self.assertEqual(schedule.end_time, PAYLOAD["end_time"])

    def test_update_schedule(self):
        """Test that a schedule can be partially updated"""

        weekday = create_weekday(name="Tuesday")
        schedule = create_schedule(**PAYLOAD)
        SectionSchedule.objects.update(weekday=weekday)
        schedule.refresh_from_db()

        self.assertEqual(schedule.section, PAYLOAD["section"])
        self.assertEqual(schedule.weekday, weekday)
        self.assertEqual(schedule.start_time, PAYLOAD["start_time"])
        self.assertEqual(schedule.end_time, PAYLOAD["end_time"])

    def test_delete_schedule(self):
        """Test that a schedule can be deleted"""

        schedule = create_schedule(**PAYLOAD)
        schedule.delete()
        schedule = SectionSchedule.objects.filter(weekday=PAYLOAD["weekday"])

        self.assertFalse(schedule.exists())

    def test_get_schedule(self):
        """Test that a schedule can be retrieved"""

        schedule = create_schedule(**PAYLOAD)
        schedule = SectionSchedule.objects.filter(section=schedule.section)

        self.assertTrue(schedule.exists())

    def test_list_schedules(self):
        """Test that all schedules can be retrieved"""

        create_schedule(**PAYLOAD)
        create_schedule(**PAYLOAD)

        schedules = SectionSchedule.objects.all()

        self.assertEqual(schedules.count(), 2)
