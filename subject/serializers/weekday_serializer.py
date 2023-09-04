from rest_framework.serializers import ModelSerializer

from ..models import Weekday


class WeekdaySerializer(ModelSerializer):
    class Meta:
        model = Weekday
        fields = ["id", "name"]
        read_only_fields = ["id"]
