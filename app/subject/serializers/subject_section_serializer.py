from rest_framework.serializers import ModelSerializer

from ..models import SubjectSection
from .subject_serializer import SubjectSerializer


class SubjectSectionSerializer(ModelSerializer):
    subject = SubjectSerializer(read_only=True)

    class Meta:
        model = SubjectSection
        exclude = ("selection",)
        read_only_fields = ("id",)
