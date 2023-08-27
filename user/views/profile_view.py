from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import ProfileSerializer

SCHEMA_NAME = "users"


@extend_schema(tags=[SCHEMA_NAME])
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id="Retrieve profile",
        description="Retrieves the requesting user profile.",
        responses={
            200: ProfileSerializer,
        },
        examples=[
            # Responses
            OpenApiExample(
                name="Retrieved profile",
                value={
                    "id": 31,
                    "first_name": "Ramón",
                    "last_name": "Ramírez",
                    "username": "r.ramirez",
                    "email": "r.ramirez@example.com",
                },
                response_only=True,
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = ProfileSerializer(user)
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
        request=ProfileSerializer,
        responses={
            200: ProfileSerializer,
        },
        examples=[
            # Requests
            OpenApiExample(
                name="Update email",
                value={
                    "email": "ramon.ramirez@example.com",
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Update password",
                value={
                    "password": "Not SO ranD0mPASSwoRd",
                },
                request_only=True,
            ),
            OpenApiExample(
                name="Update email and password",
                value={
                    "email": "ramon.ramirez@example.com",
                    "password": "Not SO cr34t1v3 P@S5W0RD",
                },
                request_only=True,
            ),
            # Responses
            OpenApiExample(
                name="Updated email",
                value={
                    "id": 31,
                    "first_name": "Ramón",
                    "last_name": "Ramírez",
                    "username": "r.ramirez",
                    "email": "ramon.ramirez@example.com",
                },
                response_only=True,
            ),
            OpenApiExample(
                name="Updated password",
                value={
                    "id": 31,
                    "first_name": "Ramón",
                    "last_name": "Ramírez",
                    "username": "r.ramirez",
                    "email": "r.ramirez@example.com",
                },
                response_only=True,
            ),
            OpenApiExample(
                name="Updated email and password",
                value={
                    "id": 31,
                    "first_name": "Ramón",
                    "last_name": "Ramírez",
                    "username": "r.ramirez",
                    "email": "ramon.ramirez@example.com",
                },
                response_only=True,
            ),
        ],
    )
    def patch(self, request, *args, **kwargs):
        try:
            user = request.user
            data = request.data
            serializer = ProfileSerializer(user, data, partial=True)

            if not serializer.is_valid():
                errors = serializer.errors
                response = {
                    "title": "Could not update the user",
                    "message": errors,
                }
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
        responses={
            204: None,
        },
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
