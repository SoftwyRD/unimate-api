from rest_framework.serializers import IntegerField, ModelSerializer

from selection.models import SelectionStarModel
from selection.serializers import SelectionSerializer


class SelectionStarSerializer(ModelSerializer):
    selection = SelectionSerializer(read_only=True)
    selection_id = IntegerField(write_only=True)

    class Meta:
        model = SelectionStarModel
        fields = ["selection", "selection_id", "starred_at"]

        read_only_fields = ["starred_at"]
