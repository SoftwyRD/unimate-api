from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Subject
from ..serializers import SubjectSerializer

SCHEMA_NAME = "subjects"


@extend_schema(tags=[SCHEMA_NAME])
class ListSubjectsView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering = ["id"]
    ordering_fields = ["id", "code", "name"]
    search_fields = ["code", "name"]
    filterset_fields = ["is_lab"]

    @extend_schema(
        operation_id="Retreave ubjects list",
        description="Retrieves all the subjects.",
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
                "title": "Internal error",
                "message": "There was an error trying to list the subjects.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def filter_queryset(self, queryset, request):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset
