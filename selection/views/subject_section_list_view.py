from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
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

from ..models import Selection, ViewHistory
from ..pagination import PageNumberPagination
from ..permissions import IsOwner

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class SubjectSectionListView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = SubjectSection.objects.all()
    serializer_class = SubjectSectionSerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    ordering = ["id"]
    ordering_fields = ["id", "subject__name", "professor"]
    search_fields = ["subject__name", "professor"]
    filterset_fields = ["selected_on__is_active"]

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
            queryset = self.get_queryset()
            self.add_view_history(request, id)
            filtered_queryset = self.filter_queryset(queryset, request)
            paginator = self.get_paginator()
            paginated_queryset = paginator.paginate_queryset(
                filtered_queryset, request
            )
            selection = self.get_selection(id)
            context = self.get_serializer_context(selection=selection)
            serializer = self.get_serializer(
                paginated_queryset, many=True, context=context
            )
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
            selection = self.get_selection(id)
            self.check_object_permissions(request, selection)
            context = self.get_serializer_context(selection=selection)
            serializer = self.get_serializer(data=request.data, context=context)
            if not serializer.is_valid():
                response = {
                    "title": "Could not add the subject section",
                    "message": serializer.errors,
                }
                return Response(response, status.HTTP_400_BAD_REQUEST)
            serializer.save()
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

    def get_selection(self, id):
        return Selection.objects.get(id=id)

    def add_view_history(self, request, id):
        page = request.query_params.get("page", None)
        if page and page != 1:
            return

        selection = self.get_selection(id)
        ViewHistory.objects.create(viewed_by=request.user, selection=selection)

    def get_serializer_context(self, **kwargs):
        selection = kwargs.pop("selection")
        return {"selection": selection}

    def get_queryset(self):
        id = self.kwargs.get("id")
        return self.queryset.filter(selected_on__selection__id=id)

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
