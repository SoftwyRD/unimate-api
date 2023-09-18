from rest_framework.serializers import IntegerField, ModelSerializer

from college.serializers import CareerSerializer

from ..models import SyllabusModel


class SyllabusSerializer(ModelSerializer):
    career = CareerSerializer(read_only=True)
    career_id = IntegerField(write_only=True)

    class Meta:
        model = SyllabusModel
        fields = [
            "id",
            "career",
            "career_id",
            "version",
            "latest",
            "credits",
            "subjects_count",
        ]

        read_only_fields = ["id", "credits"]
