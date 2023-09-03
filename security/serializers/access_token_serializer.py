from rest_framework.serializers import CharField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AccessTokenSerializer(TokenObtainPairSerializer):
    access = CharField(read_only=True)
    refresh = CharField(read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)

        return {k: data[k] for k in sorted(data)}
