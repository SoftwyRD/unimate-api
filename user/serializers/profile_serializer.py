from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    ValidationError,
)


class ProfileSerializer(ModelSerializer):
    email = CharField(min_length=5)
    password = CharField(write_only=True, min_length=9)
    password_confirm = CharField(write_only=True, min_length=9)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "password_confirm",
        ]

        read_only_fields = ["id", "first_name", "last_name", "username"]

    def validate(self, attrs):
        password = attrs.get("password", None)
        password_confirm = attrs.get("password_confirm", None)

        if password and not password_confirm:
            raise ValidationError(
                {
                    "password_confirm": (
                        "This field is required if password is present."
                    )
                }
            )

        if not password and password_confirm:
            raise ValidationError(
                {
                    "password": (
                        "This field is required if password_confirm is present."
                    )
                }
            )

        if password != password_confirm:
            raise ValidationError(
                {"password_confirm": "Passwords do not match."}
            )

        return attrs

    def validate_password(self, value):
        validate_password(value, self.instance)
        return value

    def validate_email(self, value):
        user = (
            get_user_model()
            .objects.filter(email__iexact=value)
            .exclude(id=self.instance.id)
        )
        if user.exists():
            raise ValidationError("A user with that email already exists.")
        return value

    def update(self, instance, validated_data):
        validated_data.pop("password", None)
        password = validated_data.pop("password_confirm", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
