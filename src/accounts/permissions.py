from rest_framework.permissions import BasePermission, DjangoModelPermissions

from accounts.models import User

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsOwnerOrReadOnly(BasePermission):
    """
    The user is owner, or read-only.
    """
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            obj.user == request.user
        )


class IsCandidate(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'user_type', None) == User.USER_TYPE_CANDIDATE


class IsCompany(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'user_type', None) == User.USER_TYPE_COMPANY


class IsAgency(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, 'user_type', None) == User.USER_TYPE_AGENCY


class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == User.USER_TYPE_EMPLOYEE


class IsCandidateOrReadOnly(BasePermission):
    """
    The user is candidate, or read-only.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.user_type == User.USER_TYPE_CANDIDATE
        )


class IsCompanyOrReadOnly(BasePermission):
    """
    The user is company, or read-only.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.user_type == User.USER_TYPE_COMPANY
        )


class IsAgencyOrReadOnly(BasePermission):
    """
    The user is agency, or read-only.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.user_type == User.USER_TYPE_AGENCY
        )


class IsEmployeeOrReadOnly(BasePermission):
    """
    The user is agency, or read-only.
    """
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.user_type == User.USER_TYPE_EMPLOYEE
        )


class IsCompanyOrAgency(BasePermission):
    """
    The user is agency or company, or read-only.
    """
    def has_permission(self, request, view):
        return bool(
            request.user.user_type == User.USER_TYPE_AGENCY or request.user.user_type == User.USER_TYPE_COMPANY
        )


class CustomDjangoModelPermissions(DjangoModelPermissions):

    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
