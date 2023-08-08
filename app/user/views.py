from django.urls import reverse
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import ProfileSerializer, SignUpSerializer

SCHEMA_NAME = "users"


def user_profile_url(request):
    user_profile_url = reverse("user:profile")
    absolute_url = request.build_absolute_uri(user_profile_url)
    return absolute_url


@extend_schema(tags=[SCHEMA_NAME])
class SignUpView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        operation_id="Sign up",
        description="Registers a new user.",
        request=SignUpSerializer,
        responses={
            201: SignUpSerializer,
        },
        examples=[
            # Requests
            OpenApiExample(
                name="Sign up",
                value={
                    "first_name": "Michael",
                    "last_name": "Cruz",
                    "username": "m.cruz",
                    "email": "m.cruz@example.com",
                    "password": "just_A R@nd0m-P4ssw0RD",
                },
                request_only=True,
            ),
            # Responses
            OpenApiExample(
                name="Signed up",
                value={
                    "id": 31,
                    "first_name": "Michael",
                    "last_name": "Cruz",
                    "username": "m.cruz",
                    "email": "m.cruz@example.com",
                },
                response_only=True,
                status_codes=[201],
            ),
        ],
    )
    def post(self, request, format=None):
        try:
            data = request.data
            serializer = SignUpSerializer(data=data)

            if not serializer.is_valid():
                errors = serializer.errors

                response = {
                    "title": "Could not sign up",
                    "details": errors,
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save()

            headers = {
                "Location": user_profile_url(request),
            }
            response = serializer.data
            return Response(response, status.HTTP_201_CREATED, headers=headers)

        except Exception:
            response = {
                "title": "Error",
                "message": "There was an error trying to sign up.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    def get(self, request, format=None):
        try:
            user = request.user
            serializer = ProfileSerializer(user)
            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except Exception:
            response = {
                "title": "Error",
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
    def patch(self, request, format=None):
        try:
            user = request.user
            data = request.data
            serializer = ProfileSerializer(user, data=data, partial=True)

            if not serializer.is_valid():
                response = {
                    "title": "Could not update your profile",
                    "details": serializer.errors,
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save()

            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except Exception:
            response = {
                "title": "Error",
                "message": "There was an error trying to update your profile.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Delete user profile",
        description="Deletes the requesting user profile.",
        responses={
            204: None,
        },
    )
    def delete(self, request, format=None):
        try:
            user = request.user
            user.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            response = {
                "title": "Error",
                "message": "There was an error trying to delete your profile.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
