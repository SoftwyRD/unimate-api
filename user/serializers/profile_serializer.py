from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


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
        extra_kwargs = {
            "id": {
                "read_only": True,
            },
            "first_name": {
                "read_only": True,
            },
            "last_name": {
                "read_only": True,
            },
            "username": {
                "read_only": True,
            },
            "email": {
                "min_length": 2,
            },
            "password": {
                "write_only": True,
                "min_length": 9,
            },
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
