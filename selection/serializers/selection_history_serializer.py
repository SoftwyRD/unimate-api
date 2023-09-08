from rest_framework.serializers import ModelSerializer

from .selection_serializer import SelectionSerializer

from ..models import SelectionView


class SelectionHistorySerializer(ModelSerializer):
    selection = SelectionSerializer(read_only=True)

    class Meta:
        model = SelectionView
        fields = ["selection", "created"]

        read_only_fields = ["created"]
