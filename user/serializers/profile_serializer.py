from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ValidationError


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
        )

        read_only_fields = ("id", "first_name", "last_name", "username")
        extra_kwargs = {
            "email": {
                "min_length": 5,
            },
            "password": {
                "write_only": True,
                "min_length": 9,
            },
        }

    def validate_email(self, value):
        user = get_user_model().objects.filter(email__iexact=value)
        if user.exists():
            raise ValidationError("A user with that email already exists")

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
