from rest_framework.serializers import ListSerializer
from selection.models import SectionSchedule
from selection.serializers import ScheduleSerializer


class ScheduleListSerializer(ListSerializer):
    child = ScheduleSerializer()

    class Meta:
        model = SectionSchedule
        fields = "__all__"
        read_only_fields = ["id"]
