from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenRefreshView

SCHEMA_NAME = "auth"


@extend_schema(
    tags=[SCHEMA_NAME],
)
class RefreshTokenView(TokenRefreshView):
    # @extend_schema()
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
