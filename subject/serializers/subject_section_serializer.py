from rest_framework.serializers import IntegerField, ModelSerializer

from ..models import SubjectSectionModel
from .section_schedule_serializer import SectionScheduleSerializer
from .subject_serializer import SubjectSerializer


class SubjectSectionSerializer(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    subject_id = IntegerField(write_only=True)
    schedules = SectionScheduleSerializer(read_only=True, many=True)

    class Meta:
        model = SubjectSectionModel
        fields = [
            "id",
            "subject",
            "subject_id",
            "section",
            "professor",
            "is_custom",
            "schedules",
        ]

        read_only_fields = ["id"]
