from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import PasswordSerializer

SCHEMA_NAME = "user"


@extend_schema(tags=[SCHEMA_NAME])
class PasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordSerializer

    @extend_schema(
        operation_id="Update authenticated user password",
        description="Update authenticated user password.",
        responses={
            204: None,
        },
    )
    def put(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(request.user, request.data)
            if not serializer.is_valid():
                response = serializer.errors
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying update your password.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
