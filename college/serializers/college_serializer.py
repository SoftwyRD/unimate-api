from rest_framework.serializers import ModelSerializer

from ..models import CollegeModel


class CollegeSerializer(ModelSerializer):
    class Meta:
        model = CollegeModel
        fields = ["id", "name", "full_name", "careers_count"]

        read_only_fields = ["id"]
