from rest_framework.serializers import IntegerField, ModelSerializer

from .college_serializer import CollegeSerializer

from syllabus.models import CareerModel


class CareerSerializer(ModelSerializer):
    college = CollegeSerializer(read_only=True)
    college_id = IntegerField(write_only=True)

    class Meta:
        model = CareerModel
        fields = [
            "id",
            "code",
            "name",
            "college",
            "college_id",
        ]

        read_only_fields = ["id"]
