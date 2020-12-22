"""job_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import admin_reports
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_swagger.views import get_swagger_view

from accounts.views import (
    AgencyProfileVieswSet,
    CandidateProfileVieswSet,
    CompanyProfileVieswSet,
    CustomJSONWebTokenLoginOrRequestMFACode,
    CustomJSONWebTokenLoginWithMFACode,
    EmployeeProfileViewset,
    SpecializationViewset,
    TechnologyViewset,
)
from authentication.views import RequestMFACodeView
from base.frontend.translation_settings.translation import TranslationSettingsView

router = routers.DefaultRouter()
router.register(
    'candidate_profiles',
    CandidateProfileVieswSet,
    basename='candidate_profiles'
)
router.register(
    'company_profiles',
    CompanyProfileVieswSet,
    basename='company_profiles'
)
router.register(
    'agency_profiles',
    AgencyProfileVieswSet,
    basename='agency_profiles'
)
router.register(
    'employee_profiles',
    EmployeeProfileViewset,
    basename='employee_profiles',
)
router.register('technologies', TechnologyViewset)
router.register('specializations', SpecializationViewset)

schema_view = get_swagger_view(title='GlobalIT24')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/', admin_reports.site.urls),
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/accounts/', include('accounts.urls')),
    url(r'^api/v1/accounts/team/', include('invitations.urls')),
    url(r'^api/v1/accounts/organization/', include('organization_management.urls')),
    url(r'^api/v1/accounts/me/2fa/', include('authentication.urls')),
    url(r'^api/v1/', include('authentication.urls')),
    url(r'^api/v1/token/$', CustomJSONWebTokenLoginOrRequestMFACode.as_view(), name='generate-code'),
    url(r'^api/v1/token/code/$', CustomJSONWebTokenLoginWithMFACode.as_view(), name='generate-token'),
    url(r'^api/v1/token/code/resend/$', RequestMFACodeView.as_view(), name='resend-code'),
    url(r'^api/v1/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    url(r'^api/v1/translation_setting/$', TranslationSettingsView.as_view(), name='translation_settings'),
  #   url(r'^api/v1/accounts/', include('agency_general_documents.urls')),

    # Rest API  
    url(r'^api/v1/', include('projects.urls')),
    url(r'^api/v1/', include('faq.urls')),
    url(r'^api/v1/', include('base.urls')),
    url(r'^api/v1/', include('payments.urls')),
    url(r'^api/v1/', include('authentication.urls')),
    url(r'^api/v1/', include('secure_documents.urls')),
    url(r'^', include('sitemap.urls')),
]

if settings.DEBUG or settings.TESTING:
    urlpatterns.append(
        url(r'^api/docs/', schema_view, name='swagger-docs')
    )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
