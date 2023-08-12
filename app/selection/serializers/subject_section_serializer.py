from rest_framework.serializers import ModelSerializer
from subject_section.models import SectionSchedule, SubjectSection, Weekday


class SubjectSectionSerializer(ModelSerializer):
    class Meta:
        model = SubjectSection
        exclude = ["selection"]
        read_only_fields = ["id"]

    # def update(self, instance, validated_data):
    #     schedules = validated_data.pop("subject_schedule", [])

    #     # if "subject" in validated_data:
    #     #     subject_id = validated_data["subject"]
    #     #     subject = Subject.objects.get(id=subject_id)
    #     #     validated_data["subject"] = subject
    #     return super().update(instance, validated_data)
