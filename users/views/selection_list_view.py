from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.fields import empty
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.pagination import HeaderPagination
from selection.models import SelectionModel
from selection.serializers import SelectionSerializer

SCHEMA_NAME = "users"


@extend_schema(tags=[SCHEMA_NAME])
class SelectionListView(APIView):
    authentication_classes = []
    permission_classes = (AllowAny,)
    queryset = SelectionModel.objects.all()
    serializer_class = SelectionSerializer
    pagination_class = HeaderPagination
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = ["name"]
    ordering_fields = ["name", "stars_count"]
    search_fields = ["name"]

    @extend_schema(
        operation_id="Retrieve all users",
        description="Retrieves all users.",
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
        except get_user_model().DoesNotExist:
            response = {
                "title": "User not found",
                "message": "Could not find any matching user.",
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except NotFound:
            response = {
                "title": "Out of range",
                "message": "Requested page is out of range.",
            }
            return Response(response, status.HTTP_400_BAD_REQUEST)
        except Exception:
            response = {
                "title": "Internal error",
                "message": "There was an error trying to retrieve the users.",
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_owner(self):
        username = self.kwargs.get("username")
        return get_user_model().objects.get(
            username__iexact=username, is_active=True
        )

    def get_queryset(self):
        owner = self.get_owner()
        return self.queryset.filter(owner=owner)

    def filter_queryset(self, queryset, request):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset

    def get_paginator(self):
        return self.pagination_class()

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
