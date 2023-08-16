from rest_framework.serializers import ModelSerializer
from subject.models import SubjectSection

from .subject_serializer import SubjectSerializer


class SubjectSectionSerializer(ModelSerializer):
    subject_detail = SubjectSerializer(read_only=True)

    class Meta:
        model = SubjectSection
        exclude = ("selection",)
        read_only_fields = ("id",)
        extra_kwargs = {
            "subject": {
                "write_only": True,
            }
        }
