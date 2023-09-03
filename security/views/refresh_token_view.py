from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView

SCHEMA_NAME = "auth"


@extend_schema(
    tags=[SCHEMA_NAME],
)
class RefreshTokenView(TokenRefreshView):
    @extend_schema(
        operation_id="Refresh access token",
    )
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except AuthenticationFailed:
            response = {
                "title": "Invalid token",
                "message": "Token is invalid or expired",
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            response = {
                "title": "Invalid credentials",
                "message": "No active account found with the given credentials",
            }
            return Response(
                response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
