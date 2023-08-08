from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated

from user.serializers import ProfileSerializer

SCHEMA_NAME = "users"


@extend_schema(tags=[SCHEMA_NAME])
class ProfileView(RetrieveDestroyAPIView, UpdateModelMixin):
    serializer_class = ProfileSerializer
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
        return super().get(request, *args, **kwargs)

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
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        operation_id="Delete user account",
        description="Deletes the requesting user account.",
        responses={
            204: None,
        },
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        request = self.request
        user = request.user
        return user
