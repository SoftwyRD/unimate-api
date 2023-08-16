from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Selection
from ..serializers import SelectionListSerializer

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class SelectionListView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Selection.objects.all()
    serializer_class = SelectionListSerializer
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering = ["id"]
    ordering_fields = ["id", "name", "created_on", "modified_on"]
    search_fields = ["name"]

    @extend_schema(
        operation_id="Retrieve selections list",
        description="Retrieves all the selections from the requesting user.",
        responses={
            200: serializer_class(many=True),
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.queryset
            filtered_queryset = self.filter_queryset(queryset, request)
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(
                filtered_queryset, request
            )
            serializer = self.serializer_class(paginated_queryset, many=True)
            response = paginator.get_paginated_response(serializer.data)
            return Response(response.data, status.HTTP_200_OK)
        except Exception:
            response = {
                "status": "Internal error",
                "message": "There was an error trying to list your selections.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Create selection",
        description="Retrieves all the selections from the requesting user.",
    )
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user = request.user
            context = {"user": user}
            serializer = self.serializer_class(
                data=data, many=False, context=context
            )
            if not serializer.is_valid():
                response = serializer.errors
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save(user=user)
            response = serializer.data
            headers = self.get_success_headers(response)
            return Response(response, status.HTTP_201_CREATED, headers=headers)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to create your selection.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def filter_queryset(self, queryset, request):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset

    def get_success_headers(self, response):
        id = response["id"]
        location = reverse("selection:detail", args=[id])
        headers = {
            "Location": location,
        }
        return headers
