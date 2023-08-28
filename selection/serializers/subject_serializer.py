from rest_framework.serializers import ModelSerializer

from subject.models import Subject


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"
        read_only_fields = ("id",)
