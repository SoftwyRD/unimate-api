from rest_framework.serializers import ModelSerializer
from subject.models import SubjectSection


class SubjectSectionSerializer(ModelSerializer):
    class Meta:
        model = SubjectSection
        exclude = ("selection",)
        read_only_fields = ("id",)
