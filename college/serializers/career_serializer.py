from rest_framework.serializers import ModelSerializer, IntegerField

from ..models import Career

from .college_serializer import CollegeSerializer


class CareerSerializer(ModelSerializer):
    college = CollegeSerializer(read_only=True)
    college_id = IntegerField(write_only=True)

    class Meta:
        model = Career
        fields = [
            "id",
            "name",
            "college",
            "college_id",
        ]

        read_only_fields = ["id"]
