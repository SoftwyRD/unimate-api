from django.contrib.auth import get_user_model
from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.fields import empty
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from core.pagination import HeaderPagination
from subject.models import SubjectSectionModel
from subject.serializers import SubjectSectionSerializer

from ..models import SelectionModel, ViewHistoryModel
from ..permissions import IsOwner

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class SelectionSubjectListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwner]
    queryset = SubjectSectionModel.objects.all()
    serializer_class = SubjectSectionSerializer
    pagination_class = HeaderPagination
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = ["id"]
    ordering_fields = ["id", "subject__name", "professor"]
    search_fields = ["subject__name", "professor"]

    @extend_schema(
        operation_id="Retrieve subject sections list",
        description=(
            "Retrieves all the subject sections from the specified selection."
        ),
        responses={
            200: serializer_class(many=True),
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            self.add_view_history(request)
            filtered_queryset = self.filter_queryset(queryset, request)
            paginator = self.get_paginator()
            paginated_queryset = paginator.paginate_queryset(
                filtered_queryset, request
            )
            context = self.get_serializer_context()
            serializer = self.get_serializer(
                paginated_queryset, many=True, context=context
            )
            return paginator.get_paginated_response(serializer.data)
        except (
            SelectionModel.DoesNotExist,
            SubjectSectionModel.DoesNotExist,
            PermissionDenied,
        ):
            response = {
                "title": "Subject section does not exist",
                "message": "Could not find any matching section.",
            }
            return Response(response, status.HTTP_404_NOT_FOUND)
        except NotFound:
            response = {
                "status": "Out of range",
                "message": "Requested page is out of range.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)
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
    def post(self, request, *args, **kwargs):
        try:
            selection = self.get_selection()
            self.check_object_permissions(request, selection)
            context = self.get_serializer_context()
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
            SelectionModel.DoesNotExist,
            SubjectSectionModel.DoesNotExist,
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

    def add_view_history(self, request):
        page = request.query_params.get("page", None)
        if page and page != 1:
            return

        if not request.user.is_authenticated:
            return

        selection = self.get_selection()
        ViewHistoryModel.objects.create(
            viewed_by=request.user, selection=selection
        )

    def get_serializer_context(self, **kwargs):
        selection = self.get_selection()
        return {"selection": selection}

    def get_owner(self):
        owner = self.kwargs.get("owner")
        return get_user_model().objects.get(username__iexact=owner)

    def get_selection(self):
        selection = self.kwargs.get("selection")
        owner = self.get_owner()

        user = self.request.user
        if user == owner:
            return SelectionModel.objects.get(
                slug__iexact=selection, owner=owner
            )
        return SelectionModel.objects.get(
            slug__iexact=selection, owner=owner, is_visible=True
        )

    def get_queryset(self):
        selection = self.get_selection()
        return self.queryset.filter(selections__selection=selection)

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
