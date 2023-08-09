from rest_framework.serializers import ModelSerializer
from selection.models import SectionSchedule


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = SectionSchedule
        # fields = "__all__"
        exclude = ("section", "id")
        # read_only_fields = ["id"]

    def create(self, validated_data):
        section = self.context.get("section")
        instance, created = SectionSchedule.objects.update_or_create(
            section=section, defaults=validated_data
        )
        return instance
