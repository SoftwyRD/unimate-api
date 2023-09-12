from rest_framework.serializers import IntegerField, ModelSerializer

from ..models import Syllabus
from .career_serializer import CareerSerializer


class SyllabusSerializer(ModelSerializer):
    career = CareerSerializer(read_only=True)
    career_id = IntegerField(write_only=True)

    class Meta:
        model = Syllabus
        fields = [
            "id",
            "career",
            "career_id",
            "year",
            "version",
            "credits",
            "subjects_count",
        ]

        read_only_fields = [
            "id",
            "credits",
            "subjects_count",
        ]
