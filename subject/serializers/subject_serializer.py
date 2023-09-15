from rest_framework.serializers import ModelSerializer

from college.serializers import CollegeSerializer

from ..models import SubjectModel


class SubjectSerializer(ModelSerializer):
    college = CollegeSerializer(read_only=True)

    class Meta:
        model = SubjectModel
        fields = ["id", "code", "name", "credits", "is_lab", "college"]

        read_only_fields = ["id"]
