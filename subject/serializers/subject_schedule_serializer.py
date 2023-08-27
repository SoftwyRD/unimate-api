from rest_framework.serializers import ModelSerializer
from subject.models import SectionSchedule


class SectionScheduleSerializer(ModelSerializer):
    class Meta:
        model = SectionSchedule
        exclude = ("id", "section")
        read_only_fields = ("id",)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["weekday"] = instance.weekday.name
        return representation
