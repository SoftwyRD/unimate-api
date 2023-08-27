from rest_framework.filters import BaseFilterBackend


class OwnerFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        queryset = queryset.filter(user=user)
        return queryset
