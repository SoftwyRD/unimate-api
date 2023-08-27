from rest_framework.serializers import ModelSerializer, IntegerField
from subject.models import SectionSchedule

from .weekday_serializer import WeekdaySerializer


class SectionScheduleSerializer(ModelSerializer):
    weekday = WeekdaySerializer(read_only=True)
    weekday_id = IntegerField(write_only=True)

    class Meta:
        model = SectionSchedule
        exclude = ("id", "section")
        read_only_fields = ("id",)
