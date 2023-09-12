from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import empty
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import College, Syllabus
from ..pagination import PageNumberPagination
from ..serializers import SyllabusSerializer

SCHEMA_NAME = "colleges"


@extend_schema(tags=[SCHEMA_NAME])
class CollegeSyllabusListView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering = ["career__name"]
    ordering_fields = ["career__name", "credits", "subjects_count"]
    search_fields = ["career__name"]
    filterset_fields = {
        "credits": ["exact", "gte", "lte"],
        "subjects_count": ["exact", "gte", "lte"],
    }

    @extend_schema(
        operation_id="Retrieve college's syllabuses",
        description="Retrieve college's syllabuses.",
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
        except (
            College.DoesNotExist,
            PermissionDenied,
        ):
            response = {
                "title": "College does not exist",
                "message": "Could not find any matching college.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to get the subjects.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_college(self):
        name = self.kwargs.get("name")
        return College.objects.get(name__iexact=name)

    def get_queryset(self):
        college = self.get_college()
        return self.queryset.filter(career__college=college, is_active=True)

    def filter_queryset(self, queryset, request):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset

    def get_paginator(self):
        return self.pagination_class()

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
