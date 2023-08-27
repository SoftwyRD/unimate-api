from rest_framework.serializers import ModelSerializer, IntegerField
from subject.models import SubjectSection, SectionSchedule

from .subject_serializer import SubjectSerializer
from .subject_schedule_serializer import SectionScheduleSerializer


class SubjectSectionSerializer(ModelSerializer):
    schedule = SectionScheduleSerializer(many=True)
    subject = SubjectSerializer(read_only=True)
    subject_id = IntegerField(write_only=True)

    class Meta:
        model = SubjectSection
        exclude = ("selection",)
        read_only_fields = ("id",)

    def create(self, validated_data):
        schedules = validated_data.pop("schedule", [])
        instance = super().create(validated_data)

        for schedule in schedules:
            schedule["section"] = instance
            SectionSchedule.objects.create(**schedule)

        return instance
