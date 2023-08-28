from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer


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
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "username": {
                "min_length": 2,
            },
            "email": {
                "min_length": 2,
            },
            "password": {
                "write_only": True,
                "min_length": 9,
            },
        }

    def validate(self, attrs):
        password = attrs["password"]
        validate_password(password)
        return super().validate(attrs)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
            instance.save()

        user = super().update(instance, validated_data)
        return user
