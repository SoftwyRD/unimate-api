from rest_framework.serializers import ModelSerializer

from ..models import Selection


class SelectionSerializer(ModelSerializer):
    class Meta:
        model = Selection
        exclude = ("user",)
        read_only_fields = ("id", "created_on", "modified_on")
