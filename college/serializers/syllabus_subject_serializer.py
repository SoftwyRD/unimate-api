from rest_framework.serializers import IntegerField, ModelSerializer

from ..models import SyllabusSubject
from .syllabus_serializer import SyllabusSerializer


class SyllabusSubjectSerializer(ModelSerializer):
    syllabus = SyllabusSerializer(read_only=True)
    syllabus_id = IntegerField(write_only=True)

    class Meta:
        model = SyllabusSubject
        fields = [
            "id",
            "syllabus",
            "syllabus_id",
            "cycle",
        ]

        read_only_fields = ["id"]
