from rest_framework import routers

from .views import AgencyManagementViewset, CompanyManagementViewset

router = routers.DefaultRouter()
router.register(r'agency_management', AgencyManagementViewset, basename='agency_management')
router.register(r'company_management', CompanyManagementViewset, basename='company_management')
urlpatterns = router.urls
