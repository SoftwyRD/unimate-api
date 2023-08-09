from rest_framework.serializers import ModelSerializer
from selection.models import Selection


class SelectionSerializer(ModelSerializer):
    class Meta:
        model = Selection
        fields = "__all__"
        read_only_fields = ["id", "created_on", "user"]
