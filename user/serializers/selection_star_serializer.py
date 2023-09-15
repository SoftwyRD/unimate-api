from rest_framework.serializers import IntegerField, ModelSerializer

from selection.models import SelectionStar
from selection.serializers import SelectionSerializer


class SelectionStarSerializer(ModelSerializer):
    selection = SelectionSerializer(read_only=True)
    selection_id = IntegerField(write_only=True)

    class Meta:
        model = SelectionStar
        fields = ["selection", "selection_id", "starred"]

        read_only_fields = ["starred"]
