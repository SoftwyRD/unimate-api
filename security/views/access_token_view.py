from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


SCHEMA_NAME = "auth"


@extend_schema(tags=[SCHEMA_NAME])
class AccessTokenView(TokenObtainPairView):
    @extend_schema(
        operation_id="Obtain access token",
    )
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except AuthenticationFailed:
            response = {
                "title": "Invalid credentials",
                "message": "No active account found with the given credentials",
            }
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to generate your token",
            }
            return Response(
                response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
