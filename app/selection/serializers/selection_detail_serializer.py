from rest_framework.serializers import ModelSerializer

from ..models import Selection
from .subject_section_serializer import SubjectSectionSerializer


class SelectionDetailSerializer(ModelSerializer):
    subject_section = SubjectSectionSerializer(many=True, read_only=True)

    class Meta:
        model = Selection
        exclude = ("user",)
        read_only_fields = ("id", "created_on", "modified_on")
