from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import empty
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from college.models import CollegeModel
from core.pagination import HeaderPagination

from ..models import SubjectModel, SubjectSectionModel
from ..serializers import SubjectSectionSerializer

SCHEMA_NAME = "subjects"


@extend_schema(tags=[SCHEMA_NAME])
class SubjectSectionListView(APIView):
    authentication_classes = []
    permission_classes = []
    queryset = SubjectSectionModel.objects.all()
    serializer_class = SubjectSectionSerializer
    pagination_class = HeaderPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering = ["id"]
    ordering_fields = ["id", "professor", "cycle", "year"]
    search_fields = ["professor"]
    filterset_fields = ["cycle", "year"]

    @extend_schema(
        operation_id="Retrieve subject sections",
        description="Retrieves the subject sections.",
    )
    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset()
            serializer = self.get_serializer(instance, many=True)
            response = serializer.data
            return Response(response, status=status.HTTP_200_OK)
        except (
            CollegeModel.DoesNotExist,
            SubjectModel.DoesNotExist,
            SubjectSectionModel.DoesNotExist,
            PermissionDenied,
        ):
            response = {
                "title": "Section does not exists",
                "message": "Could not find a matching section.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to retrieve the subject.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_college(self):
        college = self.kwargs.get("college")
        return CollegeModel.objects.get(name__iexact=college)

    def get_subject(self):
        subject = self.kwargs.get("subject")
        college = self.get_college()
        return SubjectModel.objects.get(code__iexact=subject, college=college)

    def get_queryset(self):
        subject = self.get_subject()
        return self.queryset.filter(subject=subject, is_custom=False)

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
