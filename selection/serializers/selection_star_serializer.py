from rest_framework.serializers import IntegerField, ModelSerializer

from ..models import SelectionStar
from .selection_serializer import SelectionSerializer


class SelectionStarSerializer(ModelSerializer):
    selection = SelectionSerializer(read_only=True)
    selection_id = IntegerField(write_only=True)

    class Meta:
        model = SelectionStar
        fields = ["selection", "selection_id", "created"]

        read_only_fields = ["created"]
