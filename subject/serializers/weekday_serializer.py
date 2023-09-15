from rest_framework.serializers import ModelSerializer

from ..models import WeekdayModel


class WeekdaySerializer(ModelSerializer):
    class Meta:
        model = WeekdayModel
        fields = ["id", "name"]

        read_only_fields = ["id"]
