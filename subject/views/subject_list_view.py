from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.fields import empty
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.pagination import HeaderPagination

from ..models import SubjectModel
from ..serializers import SubjectSerializer

SCHEMA_NAME = "subjects"


@extend_schema(tags=[SCHEMA_NAME])
class SubjectListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = SubjectModel.objects.all()
    serializer_class = SubjectSerializer
    pagination_class = HeaderPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering = ["id"]
    ordering_fields = ["id", "code", "name", "college__name"]
    search_fields = ["name"]
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
            queryset = self.get_queryset()
            filtered_queryset = self.filter_queryset(queryset, request)
            paginator = self.get_paginator()
            paginated_queryset = paginator.paginate_queryset(
                filtered_queryset, request
            )
            serializer = self.get_serializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)
        except NotFound:
            response = {
                "status": "Out of range",
                "message": "Requested page is out of range.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to list the subjects.",
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
