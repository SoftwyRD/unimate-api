from rest_framework.serializers import ModelSerializer

from ..models import SectionSchedule


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = SectionSchedule
        exclude = ["id", "section"]
