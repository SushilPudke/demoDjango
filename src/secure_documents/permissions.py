from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    The user is owner, or read-only.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.pk
