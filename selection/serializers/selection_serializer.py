from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from users.serializers import UserSerializer

from ..models import SelectionModel


class SelectionSerializer(ModelSerializer):
    full_name = SerializerMethodField()
    owner = UserSerializer(read_only=True)

    class Meta:
        model = SelectionModel
        fields = ["id", "name", "slug", "full_name", "owner", "stars_count"]

        read_only_fields = ["id", "slug", "stars_count"]

    def get_full_name(self, obj):
        return f"{obj.owner.username}/{obj.slug}"

    def validate_name(self, value):
        owner = self.context.get("owner")
        selection = SelectionModel.objects.filter(name=value, owner=owner)

        if self.instance is not None:
            selection = selection.exclude(id=self.instance.id)

        if selection.exists():
            raise ValidationError("This selection name is not available.")

        return value

    def save(self, **kwargs):
        if self.instance is None:
            owner = self.context.get("owner")
            kwargs.update(owner=owner)
        return super().save(**kwargs)
