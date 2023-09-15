from rest_framework.serializers import ModelSerializer


from ..models import SubjectModel


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = SubjectModel
        fields = ["id", "code", "name", "credits", "is_lab"]

        read_only_fields = ["id"]
