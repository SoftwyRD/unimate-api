from rest_framework.serializers import ModelSerializer

from subject.models import Weekday


class WeekdaySerializer(ModelSerializer):
    class Meta:
        model = Weekday
        fields = "__all__"
        read_only_fields = ("id",)
