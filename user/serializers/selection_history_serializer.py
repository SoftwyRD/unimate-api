from rest_framework.serializers import ModelSerializer

from selection.serializers import SelectionSerializer

from selection.models import ViewHistoryModel


class SelectionHistorySerializer(ModelSerializer):
    selection = SelectionSerializer(read_only=True)

    class Meta:
        model = ViewHistoryModel
        fields = ["selection", "viewed_at"]

        read_only_fields = ["viewed_at"]
