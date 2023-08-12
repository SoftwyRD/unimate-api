from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        is_owner = obj.selection.user == user
        return is_owner
