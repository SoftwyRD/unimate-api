from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers import SignUpSerializer

SCHEMA_NAME = "auth"


@extend_schema(tags=[SCHEMA_NAME])
class SignUpView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer

    @extend_schema(
        operation_id="Sign up",
        description="Registers a new user.",
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                response = serializer.errors
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save()
            headers = self.get_success_headers()
            response = serializer.data
            return Response(response, status.HTTP_201_CREATED, headers=headers)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to sign you up.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_success_headers(self):
        location = reverse("user:profile")
        headers = {
            "Location": location,
        }
        return headers
