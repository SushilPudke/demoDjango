from django.urls import path
from rest_framework import routers

from .views import (UploadCompanySecureDocumentView, CompanySecureDocumentViewset,
                    UploadCompanyGeneralDocumentsView, RetrieveUpdateCompanyGeneralDocumentsView,
                    UploadCandidateGeneralDocumentsView, RetrieveUpdateCandidateGeneralDocumentsView,
                    CandidateSecureDocumentViewset, UploadCandidateSecureDocumentView,
                    CompanyGeneralDocumentsViewSet, CandidateGeneralDocumentsViewSet,
                    AgencySecureDocumentViewset, AgencyGeneralDocumentsViewSet,
                    UploadAgencySecureDocumentView)


router = routers.DefaultRouter()

router.register('company_secure_documents', CompanySecureDocumentViewset, basename='company_secure_documents')
router.register('company_general_documents', CompanyGeneralDocumentsViewSet, basename='company_general_documents')
router.register('candidate_secure_documents', CandidateSecureDocumentViewset, basename='candidate_secure_documents')
router.register('candidate_general_documents', CandidateGeneralDocumentsViewSet, basename='candidate_general_documents')
router.register('agency_secure_documents', AgencySecureDocumentViewset, basename='agency_secure_documents')
router.register('agency_general_documents', AgencyGeneralDocumentsViewSet, basename='agency_general_documents')

urlpatterns = [
     path('upload_agency_secure_document/', UploadAgencySecureDocumentView.as_view(),
          name='upload_agency_secure_documents'),
     path('upload_company_secure_document/', UploadCompanySecureDocumentView.as_view(),
          name='upload_company_secure_documents'),
     path('upload_company_general_documents/', UploadCompanyGeneralDocumentsView.as_view(),
          name='upload_company_general_documents'),
     path('update_company_general_documents/', RetrieveUpdateCompanyGeneralDocumentsView.as_view(),
          name='update_company_general_documents'),
     path('upload_candidate_secure_document/', UploadCandidateSecureDocumentView.as_view(),
          name='upload_candidate_secure_documents'),
     path('upload_candidate_general_documents/', UploadCandidateGeneralDocumentsView.as_view(),
          name='upload_candidate_general_documents'),
     path('update_candidate_general_documents/', RetrieveUpdateCandidateGeneralDocumentsView.as_view(),
          name='update_candidate_general_documents'),
]

urlpatterns += router.urls
