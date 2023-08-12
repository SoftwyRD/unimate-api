from django.urls import reverse
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import SignUpSerializer

SCHEMA_NAME = "users"


@extend_schema(tags=[SCHEMA_NAME])
class SignUpView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    @extend_schema(
        operation_id="Sign up",
        auth=[],
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
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = SignUpSerializer(data=data)

            if not serializer.is_valid():
                response = {
                    "title": "Could not register the user",
                    "message": serializer.errors,
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)

            serializer.save()
            headers = self.get_success_headers()
            response = serializer.data
            return Response(response, status.HTTP_201_CREATED, headers=headers)

        except Exception:
            response = {
                "title": "error",
                "message": "There was an error trying to sign you up.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_success_headers(self):
        location = reverse("user:profile")
        headers = {
            "Location": location,
        }
        return headers
