from rest_framework.serializers import ModelSerializer

from user.serializers import ProfileSerializer

from ..models import Selection


class SelectionSerializer(ModelSerializer):
    user = ProfileSerializer(read_only=True)

    class Meta:
        model = Selection
        fields = ["id", "user", "name", "created", "modified"]

        read_only_fields = ["id", "created", "modified"]
