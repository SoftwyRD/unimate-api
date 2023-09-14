from rest_framework.serializers import ModelSerializer

from user.serializers import UserSerializer

from ..models import Selection


class SelectionSerializer(ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Selection
        fields = ["id", "name", "owner", "stars_count"]

        read_only_fields = ["id"]
