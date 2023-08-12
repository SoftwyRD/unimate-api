from rest_framework.serializers import ModelSerializer

from ..models import SectionSchedule


class ScheduleListSerializer(ModelSerializer):
    class Meta:
        model = SectionSchedule
        fields = "__all__"
        read_only_fields = ["id"]
