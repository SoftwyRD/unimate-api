from rest_framework.serializers import CharField
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


class RefreshTokenSerializer(TokenRefreshSerializer):
    refresh = CharField(write_only=True)
