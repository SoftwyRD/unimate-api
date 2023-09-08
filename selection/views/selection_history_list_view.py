from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.fields import empty
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import SelectionView
from ..pagination import PageNumberPagination
from ..serializers import SelectionHistorySerializer

SCHEMA_NAME = "selections"


@extend_schema(tags=[SCHEMA_NAME])
class SelectionHistoryListView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = SelectionView.objects.all()
    serializer_class = SelectionHistorySerializer
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = ["-created"]
    search_fields = ["selection__name"]

    @extend_schema(
        operation_id="Retrieve selections history",
        description="Retrieves selections history.",
        responses={
            200: serializer_class(many=True),
        },
    )
    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            paginator = self.get_paginator()
            filtered_queryset = self.filter_queryset(queryset, request)
            paginated_queryset = paginator.paginate_queryset(
                filtered_queryset, request
            )
            serializer = self.get_serializer(paginated_queryset, many=True)
            response = paginator.get_paginated_response(serializer.data)
            return Response(response, status.HTTP_200_OK)
        except Exception:
            response = {
                "title": "Internal error",
                "message": (
                    "There was an error trying to update your selection."
                ),
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_queryset(self):
        return self.queryset.filter(viewed_by=self.request.user)

    def filter_queryset(self, queryset, request):
        for backend in self.filter_backends:
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset

    def get_paginator(self):
        return self.pagination_class()

    def get_serializer(self, instance=None, data=empty, **kwargs):
        return self.serializer_class(instance, data, **kwargs)
