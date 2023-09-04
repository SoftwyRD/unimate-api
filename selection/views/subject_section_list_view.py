from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import empty
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from subject.models import SubjectSection
from subject.serializers import SubjectSectionSerializer

from ..models import Selection
from ..pagination import PageNumberPagination
from ..permissions import IsOwner

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class SubjectSectionListView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = SubjectSection.objects.all()
    serializer_class = SubjectSectionSerializer
    pagination_class = PageNumberPagination
    filter_backends = [OrderingFilter, SearchFilter]
    ordering = ["id"]
    ordering_fields = ["id", "subject__name", "professor"]
    search_fields = ["subject__name", "professor"]
    filterset_fields = ["is_taken"]

    @extend_schema(
        operation_id="Retrieve subject sections list",
        description=(
            "Retrieves all the subject sections from the specified selection."
        ),
        responses={
            200: serializer_class(many=True),
        },
    )
    def get(self, request, id, *args, **kwargs):
        try:
            instance = self.get_obj(id)
            self.check_object_permissions(request, instance)
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
            instance = self.get_obj(id)
            self.check_object_permissions(request, instance)
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                response = {
                    "title": "Could not add the subject section",
                    "message": serializer.errors,
                }
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
        except Exception:
            response = {
                "title": "Internal error",
                "message": (
                    "There was an error trying to add the subject section."
                ),
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_obj(self, id):
        return Selection.objects.get(id=id)

    def get_queryset(self):
        id = self.kwargs.get("id")
        instance = self.get_obj(id)
        return self.queryset.filter(selection=instance)

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
        location = reverse("subject:sections", args=[id])
        headers = {
            "Location": location,
        }
        return headers
