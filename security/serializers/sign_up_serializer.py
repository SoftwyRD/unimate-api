from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, ValidationError


class SignUpSerializer(ModelSerializer):
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

        read_only_fields = ("id",)
        extra_kwargs = {
            "username": {
                "min_length": 2,
            },
            "email": {
                "min_length": 5,
            },
            "password": {
                "write_only": True,
                "min_length": 9,
            },
        }

    def validate_username(self, value):
        user = get_user_model().objects.filter(username__iexact=value)
        if user.exists():
            raise ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        user = get_user_model().objects.filter(email__iexact=value)
        if user.exists():
            raise ValidationError("A user with that email already exists.")
        return value

    def validate_password(self, value):
        validate_password(value)
