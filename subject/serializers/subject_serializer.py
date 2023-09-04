from rest_framework.serializers import ModelSerializer

from ..models import Subject


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "code", "name", "credits", "is_lab"]
        read_only_fields = ["id"]
