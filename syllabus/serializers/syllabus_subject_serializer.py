from rest_framework.serializers import IntegerField, ModelSerializer

from ..models import SyllabusSubjectModel
from .syllabus_serializer import SyllabusSerializer

from subject.serializers import SubjectSerializer


class SyllabusSubjectSerializer(ModelSerializer):
    subject = SubjectSerializer(read_only=True)
    syllabus = SyllabusSerializer(read_only=True)
    syllabus_id = IntegerField(write_only=True)

    class Meta:
        model = SyllabusSubjectModel
        fields = ["id", "subject", "syllabus", "syllabus_id", "cycle"]

        read_only_fields = ["id"]
