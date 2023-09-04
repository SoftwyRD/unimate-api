from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.fields import empty
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..filters import OwnerFilter
from ..models import Selection
from ..pagination import PageNumberPagination
from ..serializers import SelectionSerializer

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class SelectionListView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Selection.objects.all()
    serializer_class = SelectionSerializer
    pagination_class = PageNumberPagination
    filter_backends = [OwnerFilter, OrderingFilter, SearchFilter]
    ordering = ["id"]
    ordering_fields = ["id", "name", "created", "modified"]
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
            queryset = self.get_queryset()
            filtered_queryset = self.filter_queryset(queryset, request)
            paginator = self.get_paginator()
            paginated_queryset = paginator.paginate_queryset(
                filtered_queryset, request
            )
            serializer = self.get_serializer(paginated_queryset, many=True)
            response = paginator.get_paginated_response(serializer.data)
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
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
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                response = {
                    "title": "Could not create the selection",
                    "message": serializer.errors,
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user)
            response = serializer.data
            headers = self.get_success_headers(response)
            return Response(response, status.HTTP_201_CREATED, headers=headers)
        except Exception:
            response = {
                "title": "Internal error",
                "message": (
                    "There was an error trying to create your selection."
                ),
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        return self.queryset

    def filter_queryset(self, queryset, request):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset

    def get_paginator(self):
        return self.pagination_class()

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)

    def get_success_headers(self, response):
        id = response["id"]
        location = reverse("selection:detail", args=[id])
        headers = {
            "Location": location,
        }
        return headers
