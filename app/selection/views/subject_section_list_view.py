from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from subject.models import SubjectSection

from ..models import Selection
from ..permissions import IsOwner
from ..serializers import SubjectSectionSerializer

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class SubjectSectionListView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = SubjectSection.objects.all()
    serializer_class = SubjectSectionSerializer
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering = ("id",)
    ordering_fields = ("id", "subject__name", "professor")
    search_fields = ("subject__name", "professor")
    filterset_fields = ("is_taken",)

    @extend_schema(
        operation_id="Retrieve subject sections list",
        description="Retrieves all the subject sections from the specified selection.",
        responses={
            200: serializer_class(many=True),
        },
    )
    def get(self, request, id, *args, **kwargs):
        try:
            instance = Selection.objects.get(id=id)
            self.check_object_permissions(request, instance)
            queryset = self.queryset.filter(selection=instance)
            filtered_queryset = self.filter_queryset(queryset, request)
            paginator = self.pagination_class()
            paginated_queryset = paginator.paginate_queryset(
                filtered_queryset, request
            )
            serializer = self.serializer_class(paginated_queryset, many=True)
            response = paginator.get_paginated_response(serializer.data)
            return Response(response.data, status=status.HTTP_200_OK)
        except (
            Selection.DoesNotExist,
            SubjectSection.DoesNotExist,
            PermissionDenied,
        ):
            response = {
                "title": "Subject section does not exist",
                "message": "Could not find any matching section.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to get the subjects.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    @extend_schema(
        operation_id="Add subject section",
        description="Adds a subject section to the specified selections.",
    )
    def post(self, request, id, *args, **kwargs):
        try:
            instance = Selection.objects.get(id=id)
            self.check_object_permissions(request, instance)
            data = request.data
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                response = serializer.errors
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save(selection=instance)
            response = serializer.data
            headers = self.get_success_headers(response)
            return Response(response, status.HTTP_201_CREATED, headers=headers)
        except (
            Selection.DoesNotExist,
            SubjectSection.DoesNotExist,
            PermissionDenied,
        ):
            response = {
                "title": "Subject section does not exist",
                "message": "Could not find any matching section.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            response = {
                "title": "Internal error",
                "message": "There was an error trying to add the subject section.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def filter_queryset(self, queryset, request):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset

    def get_success_headers(self, response):
        id = response["id"]
        location = reverse("subject:section-detail", args=[id])
        headers = {
            "Location": location,
        }
        return headers
