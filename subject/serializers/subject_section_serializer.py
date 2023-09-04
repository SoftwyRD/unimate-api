from rest_framework.serializers import IntegerField, ModelSerializer

from ..models import SectionSchedule, SubjectSection
from .section_schedule_serializer import SectionScheduleSerializer
from .subject_serializer import SubjectSerializer


class SubjectSectionSerializer(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    subject_id = IntegerField(write_only=True)
    schedules = SectionScheduleSerializer(required=False, many=True)

    class Meta:
        model = SubjectSection
        fields = [
            "id",
            "subject",
            "subject_id",
            "section",
            "professor",
            "taken",
            "schedules",
        ]

        read_only_fields = ["id"]

    def create(self, validated_data):
        schedules = validated_data.pop("schedules", [])
        instance = super().create(validated_data)

        for schedule in schedules:
            schedule["section"] = instance
            SectionSchedule.objects.create(**schedule)

        return instance

    def update(self, instance, validated_data):
        schedules = validated_data.pop("schedules", [])
        instance = super().update(instance, validated_data)

        for schedule in instance.schedules.all():
            schedule.delete()

        for schedule in schedules:
            schedule["section"] = instance
            SectionSchedule.objects.create(**schedule)

        return instance
