from django.urls import include, path
from rest_framework import routers

from accounts.views import (
    AccountInfoAPiView,
    ActivateView,
    AgencyCandidateCVViewset,
    ChangeEmailView,
    ChangePasswordView,
    CheckEmailView,
    CreateUserAPIView,
    CVViewset,
    DeleteAccountView,
    IdentificateCandidateProfileView,
    UploadCompanyDocumentView,
    UploadCVView,
)

router = routers.DefaultRouter()
router.register(r'candidate_cvs', CVViewset, basename='candidate_cvs')
router.register(r'agency_candidate_cvs', AgencyCandidateCVViewset, basename='agency_candidate_cvs')
urlpatterns = router.urls


urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('secure_documents.urls')),
    path('create/', CreateUserAPIView.as_view(), name='create'),
    path('me/', AccountInfoAPiView.as_view(), name='me'),
    path('delete/', DeleteAccountView.as_view(), name='delete_account'),
    path('check_email/', CheckEmailView.as_view(), name='check_email'),
    path('change_email/<uidb64>/<token>/<email>/', ChangeEmailView.as_view(), name='change_email'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('upload_cv/', UploadCVView.as_view(), name='upload_cv'),
    path('upload_document/', UploadCompanyDocumentView.as_view(), name='upload_document'),
    path('identificate_candidate/', IdentificateCandidateProfileView.as_view(), name='identificate_candidate'),
    path('password_reset/', include('accounts.password_reset_urls', namespace='password_reset')),
]

urlpatterns = urlpatterns + router.urls
