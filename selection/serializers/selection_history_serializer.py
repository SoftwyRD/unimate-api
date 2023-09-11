from rest_framework.serializers import ModelSerializer

from .selection_serializer import SelectionSerializer

from ..models import ViewHistory


class SelectionHistorySerializer(ModelSerializer):
    selection = SelectionSerializer(read_only=True)

    class Meta:
        model = ViewHistory
        fields = ["selection", "viewed"]

        read_only_fields = ["viewed"]
