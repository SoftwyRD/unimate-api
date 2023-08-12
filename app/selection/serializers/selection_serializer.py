from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from ..models import Selection


class SelectionSerializer(ModelSerializer):
    class Meta:
        model = Selection
        exclude = ["user"]
        read_only_fields = ["id", "created_on", "modified_on"]

    def validate(self, attrs):
        if not self.context:
            return attrs

        user = self.context["user"]
        name = attrs["name"]
        selection = Selection.objects.filter(user=user, name=name)
        if not selection.exists():
            return attrs

        validation_error = {"name": "There is a selection with that name."}
        raise ValidationError(validation_error)
