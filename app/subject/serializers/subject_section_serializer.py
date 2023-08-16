from rest_framework.serializers import ModelSerializer

from ..models import SubjectSection, SectionSchedule
from .subject_serializer import SubjectSerializer
from .subject_schedule_serializer import SectionScheduleSerializer


class SubjectSectionSerializer(ModelSerializer):
    schedule = SectionScheduleSerializer(many=True)

    class Meta:
        model = SubjectSection
        exclude = ("selection",)
        read_only_fields = ("id",)

    def update(self, instance, validated_data):
        schedules = validated_data.pop("schedule", [])
        instance = super().update(instance, validated_data)

        for schedule in instance.schedule.all():
            schedule.delete()

        for schedule in schedules:
            schedule["section"] = instance
            SectionSchedule.objects.create(**schedule)

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        serializer = SubjectSerializer(instance.subject)
        representation["subject"] = serializer.data
        return representation
