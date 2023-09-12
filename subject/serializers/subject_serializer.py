from rest_framework.serializers import ModelSerializer

from college.serializers import SyllabusSubjectSerializer

from ..models import Subject


class SubjectSerializer(ModelSerializer):
    syllabuses = SyllabusSubjectSerializer(read_only=True, many=True)

    class Meta:
        model = Subject
        fields = ["id", "code", "name", "credits", "is_lab", "syllabuses"]

        read_only_fields = ["id"]
