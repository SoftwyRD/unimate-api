from rest_framework.serializers import ModelSerializer

from ..models import Selection


class SelectionSerializer(ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name", "created", "modified"]

        read_only_fields = ["id", "created", "modified"]
