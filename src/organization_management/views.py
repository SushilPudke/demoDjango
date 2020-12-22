from rest_framework.permissions import IsAuthenticated
from rest_framework_guardian.filters import ObjectPermissionsFilter

from accounts.permissions import CustomDjangoModelPermissions
from accounts.views import AgencyProfileVieswSet, CompanyProfileVieswSet


class AgencyManagementViewset(AgencyProfileVieswSet):
    permission_classes = [CustomDjangoModelPermissions, IsAuthenticated]
    filter_backends = [ObjectPermissionsFilter]


class CompanyManagementViewset(CompanyProfileVieswSet):
    permission_classes = [CustomDjangoModelPermissions, IsAuthenticated]
    filter_backends = [ObjectPermissionsFilter]
