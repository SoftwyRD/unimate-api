from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import ProfileSerializer

SCHEMA_NAME = "users"


@extend_schema(tags=[SCHEMA_NAME])
class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    @extend_schema(
        operation_id="Retrieve profile",
        description="Retrieves the requesting user profile.",
    )
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = self.serializer_class(user)
            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to retrieve your profile.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Partial update user profile",
        description="Partially updates the requesting user profile.",
    )
    def patch(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data
            serializer = self.serializer_class(user, data, partial=True)
            if not serializer.is_valid():
                response = serializer.errors
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save()
            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to update your profile.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Delete user account",
        description="Deletes the requesting user account.",
    )
    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to delete your profile.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
