from django.urls import reverse
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from user.serializers import SignUpSerializer

SCHEMA_NAME = "users"


def user_profile_url(request):
    user_profile_url = reverse("user:profile")
    absolute_url = request.build_absolute_uri(user_profile_url)
    return absolute_url


@extend_schema(tags=[SCHEMA_NAME])
class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
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
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_success_headers(self, data):
        location = reverse("user:profile")
        return {"Location": location}
