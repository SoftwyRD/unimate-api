from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, ModelSerializer


class ProfileSerializer(ModelSerializer):
    email = CharField(min_length=5)

    class Meta:
        model = get_user_model()
        fields = ["id", "first_name", "last_name", "username", "email"]

        read_only_fields = ["id", "first_name", "last_name", "username"]
