from rest_framework.serializers import (
    BooleanField,
    IntegerField,
    ModelSerializer,
)

from ..models import SectionSchedule, SelectedSection, SubjectSection
from .section_schedule_serializer import SectionScheduleSerializer
from .subject_serializer import SubjectSerializer


class SubjectSectionSerializer(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    subject_id = IntegerField(write_only=True)
    schedules = SectionScheduleSerializer(required=False, many=True)
    is_active = BooleanField(required=False)

    class Meta:
        model = SubjectSection
        fields = [
            "id",
            "subject",
            "subject_id",
            "section",
            "professor",
            "is_active",
            "schedules",
        ]

        read_only_fields = ["id"]

    def create(self, validated_data):
        schedules = validated_data.pop("schedules", [])
        is_active = validated_data.pop("is_active", True)
        instance = super().create(validated_data)

        for schedule in schedules:
            schedule["section"] = instance
            SectionSchedule.objects.create(**schedule)

        selection = self.context.get("selection")
        SelectedSection.objects.create(
            selection=selection, section=instance, is_active=is_active
        )

        return instance

    def update(self, instance, validated_data):
        schedules = validated_data.pop("schedules", [])
        is_active = validated_data.pop("is_active", None)
        instance = super().update(instance, validated_data)

        for schedule in instance.schedules.all():
            schedule.delete()

        for schedule in schedules:
            schedule["section"] = instance
            SectionSchedule.objects.create(**schedule)

        selection = self.context.get("selection")
        section = SelectedSection.objects.get(
            selection=selection, section=instance
        )

        if is_active is not None:
            section.is_active = is_active
            section.save()

        return instance

    def to_representation(self, instance):
        selection = self.context.get("selection")
        section = SelectedSection.objects.get(
            selection=selection, section=instance
        )
        instance.is_active = section.is_active
        return super().to_representation(instance)
