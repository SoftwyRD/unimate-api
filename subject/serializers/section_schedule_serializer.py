from rest_framework.serializers import ModelSerializer, IntegerField

from ..models import SectionSchedule
from .weekday_serializer import WeekdaySerializer


class SectionScheduleSerializer(ModelSerializer):
    weekday = WeekdaySerializer(read_only=True)
    weekday_id = IntegerField(write_only=True)

    class Meta:
        model = SectionSchedule
        fields = ["weekday", "weekday_id", "start_time", "end_time"]
