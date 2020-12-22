from rest_framework.permissions import BasePermission
from django.core.exceptions import ObjectDoesNotExist


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class PositionProjectIsOwnerOrReadOnly(BasePermission):
    """
    The users compamy profile is owner, or read-only.
    """
    def has_object_permission(self, request, view, obj):
        try:
            company = request.user.company_profile
        except (ObjectDoesNotExist, AttributeError):
            company = None
        return bool(
            request.method in SAFE_METHODS or
            obj.company == company
        )


class HasCompanyProfileOrReadOnly(BasePermission):
    """
    Company has profile or read-only
    """
    def has_permission(self, request, view):
        try:
            company = request.user.company_profile
        except (ObjectDoesNotExist, AttributeError):
            company = None
        return bool(
            request.method in SAFE_METHODS or
            company is not None
        )


class HasCompanyProfile(BasePermission):
    """
    Allows access only to users with company profile
    """
    def has_permission(self, request, view):
        try:
            company = request.user.company_profile
        except (ObjectDoesNotExist, AttributeError):
            company = None
        return bool(company is not None)


class HasCandidateProfile(BasePermission):
    """
    Allows access only to users with candidate profile
    """
    def has_permission(self, request, view):
        try:
            candidate = request.user.candidate_profile
        except (ObjectDoesNotExist, AttributeError):
            candidate = None
        return bool(candidate is not None)


class HasCandidateOrAgencyProfile(BasePermission):
    """
    Allows access only to users with candidate of agency profile
    """
    def has_permission(self, request, view):
        try:
            candidate = request.user.candidate_profile
        except (ObjectDoesNotExist, AttributeError):
            candidate = None
        try:
            agency = request.user.agency_profile
        except (ObjectDoesNotExist, AttributeError):
            agency = None
        return bool(candidate is not None or agency is not None)


class HasAgencyProfile(BasePermission):
    """
    Allows access only to users with agency profile
    """
    def has_permission(self, request, view):
        try:
            agency = request.user.agency_profile
        except (ObjectDoesNotExist, AttributeError):
            agency = None
        return bool(agency is not None)
