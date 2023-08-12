from rest_framework.filters import BaseFilterBackend


class OwnerFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        queryset = queryset.filter(selection__user=user)
        return queryset
