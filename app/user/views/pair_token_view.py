from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView

SCHEMA_NAME = "users"


@extend_schema(
    tags=[SCHEMA_NAME],
)
class PairTokenView(TokenObtainPairView):
    # @extend_schema()
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
