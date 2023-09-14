from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.fields import empty
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from college.models import College

from ..models import Career, Syllabus
from ..pagination import PageNumberPagination
from ..serializers import SyllabusSerializer

SCHEMA_NAME = "syllabuses"


@extend_schema(tags=[SCHEMA_NAME])
class SyllabusListView(APIView):
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
        except College.DoesNotExist:
            response = {
                "title": "College does not exist",
                "message": "Could not find any matching college.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Career.DoesNotExist:
            response = {
                "title": "Career does not exist",
                "message": "Could not find any matching career.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except NotFound:
            response = {
                "title": "Out of range",
                "message": "Requested page is out of range.",
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to get the subjects.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_college(self):
        college = self.kwargs.get("college")
        return College.objects.get(name__iexact=college)

    def get_career(self):
        code = self.kwargs.get("code")
        college = self.get_college()
        return Career.objects.get(college=college, code__iexact=code)

    def get_queryset(self):
        career = self.get_career()
        return self.queryset.filter(career=career, is_active=True)

    def filter_queryset(self, queryset, request):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset

    def get_paginator(self):
        return self.pagination_class()

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
