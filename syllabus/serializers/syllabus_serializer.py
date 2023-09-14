from rest_framework.serializers import IntegerField, ModelSerializer

from ..models import Syllabus
from college.serializers import CareerSerializer


class SyllabusSerializer(ModelSerializer):
    career = CareerSerializer(read_only=True)
    career_id = IntegerField(write_only=True)
    subjects = IntegerField(read_only=True, source="subjects_count")

    class Meta:
        model = Syllabus
        fields = [
            "id",
            "career",
            "career_id",
            "version",
            "credits",
            "subjects",
        ]

        read_only_fields = [
            "id",
            "credits",
        ]
