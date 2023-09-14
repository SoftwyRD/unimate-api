from rest_framework.serializers import ModelSerializer

from ..models import College


class CollegeSerializer(ModelSerializer):
    class Meta:
        model = College
        fields = ["id", "name", "full_name", "careers_count"]

        read_only_fields = ["id"]
