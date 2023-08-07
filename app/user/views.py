from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserSerializer

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
        request=UserSerializer,
        responses={
            201: UserSerializer,
        },
    )
    def post(self, request, format=None):
        try:
            data = request.data
            serializer = UserSerializer(data=data)

            if not serializer.is_valid():
                response = {
                    "title": "Could not sign up",
                    "details": serializer.errors,
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
        request=UserSerializer,
        responses={
            200: UserSerializer,
        },
    )
    def get(self, request, format=None):
        try:
            user = request.user
            serializer = UserSerializer(user)
            response = serializer.data
            return Response(response, status.HTTP_200_OK)
        except Exception:
            response = {
                "title": "Error",
                "message": "There was an error trying to retrieve your profile.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Update user profile",
        description="Updates the requesting user profile.",
        request=UserSerializer,
        responses={
            200: UserSerializer,
        },
    )
    def put(self, request, format=None):
        try:
            user = request.user
            data = request.data
            serializer = UserSerializer(user, data=data)

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
        operation_id="Partial update user profile",
        description="Partially updates the requesting user profile.",
        request=UserSerializer,
        responses={
            200: UserSerializer,
        },
    )
    def patch(self, request, format=None):
        try:
            user = request.user
            data = request.data
            serializer = UserSerializer(user, data=data, partial=True)

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
