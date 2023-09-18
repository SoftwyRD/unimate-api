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
    visibility = SerializerMethodField()

    class Meta:
        model = SelectionModel
        fields = [
            "id",
            "name",
            "slug",
            "full_name",
            "owner",
            "stars_count",
            "is_visible",
            "visibility",
            "created_at",
            "modified_at",
        ]

        read_only_fields = [
            "id",
            "slug",
            "stars_count",
            "created_at",
            "modified_at",
        ]

    def get_full_name(self, obj):
        return f"{obj.owner.username}/{obj.slug}"

    def get_visibility(self, obj):
        return "Visible" if obj.is_visible else "Hidden"

    def validate_name(self, value):
        owner = self.context.get("owner")
        selection = SelectionModel.objects.filter(
            name__iexact=value, owner=owner
        )

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
