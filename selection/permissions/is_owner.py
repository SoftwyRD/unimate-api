from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return obj.is_visible

        if obj.owner == request.user:
            return True

        return obj.is_visible and request.method in SAFE_METHODS
