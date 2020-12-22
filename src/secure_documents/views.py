import mimetypes
import os

from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from storages.backends.sftpstorage import SFTPStorage

from accounts.permissions import IsAgency, IsCandidate, IsCompany

from .models import (
    AgencyGeneralDocuments,
    AgencySecureDocument,
    CandidateGeneralDocuments,
    CandidateSecureDocument,
    CompanyGeneralDocuments,
    CompanySecureDocument,
)
from .permissions import IsOwner
from .serializers import (
    AgencyGeneralDocumentsSerializer,
    AgencySecureDocumentSerializer,
    CandidateGeneralDocumentsSerializer,
    CandidateSecureDocumentSerializer,
    CompanyGeneralDocumentsSerializer,
    CompanySecureDocumentSerializer,
    RetrieveUpdateCandidateGeneralDocumentsSerializer,
    RetrieveUpdateCompanyGeneralDocumentsSerializer,
    UploadAgencySecureDocumentSerializer,
    UploadCandidateSecureDocumentSerializer,
    UploadCompanySecureDocumentSerializer,
)
from .validators import ChangeFieldValidator

STORAGE = SFTPStorage()


class UploadCompanyGeneralDocumentsView(generics.CreateAPIView):
    """
    Endpoint for Company to upload general documents
    """
    serializer_class = CompanyGeneralDocumentsSerializer
    permission_classes = (IsAuthenticated, IsCompany, IsOwner)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        if CompanyGeneralDocuments.objects.filter(user_id=user_id).exists():
            return Response(
                {'status': _('You cannot upload data one more time. To change it, please contact us.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UploadCandidateGeneralDocumentsView(generics.CreateAPIView):
    """
    Endpoint for Candidate to upload general documents
    """
    serializer_class = CandidateGeneralDocumentsSerializer
    permission_classes = (IsAuthenticated, IsCandidate, IsOwner)

    def post(self, request, *args, **kwargs):
        user_id = request.user.id
        if CandidateGeneralDocuments.objects.filter(user_id=user_id).exists():
            return Response(
                {'status': _('You cannot upload data one more time. To change it, please contact us.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateCompanyGeneralDocumentsView(generics.RetrieveUpdateAPIView):
    serializer_class = RetrieveUpdateCompanyGeneralDocumentsSerializer
    permission_classes = (IsAuthenticated, IsCompany, IsOwner)

    def get_object(self):
        user_id = self.request.user.id
        return get_object_or_404(CompanyGeneralDocuments, user_id=user_id)

    def put(self, request, *args, **kwargs):
        for field in request.data:
            ChangeFieldValidator.validate(self, field=field)
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        for field in request.data:
            ChangeFieldValidator.validate(self, field=field)
        return super().partial_update(request, *args, **kwargs)


class CompanyGeneralDocumentsViewSet(viewsets.ModelViewSet):
    serializer_class = CompanyGeneralDocumentsSerializer
    permission_classes = (IsAuthenticated, IsCompany)

    def get_queryset(self):
        user_id = self.request.user.id
        return CompanyGeneralDocuments.objects.filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        """POST create company general documents object"""
        user_id = request.user.id
        if CompanyGeneralDocuments.objects.filter(user_id=user_id).exists():
            return Response(
                {'status': _('You cannot upload data one more time. To change it, please contact us.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """PUT update company general documents object"""
        for field in request.data:
            ChangeFieldValidator.validate(self, field=field)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """PATCH update company general documents object"""
        for field in request.data:
            ChangeFieldValidator.validate(self, field=field)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        response = {"detail": _("You do not have permission to perform this action.")}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get'], detail=True)
    def download_tax_number_document(self, request, pk=None):
        """GET download tax number document"""
        try:
            obj = CompanyGeneralDocuments.objects.get(id=pk, user_id=request.user.pk)
        except CompanyGeneralDocuments.DoesNotExist:
            raise Http404

        if obj.tax_number_document.name:
            if STORAGE.exists(name=obj.tax_number_document.name):
                file = STORAGE._read(name=obj.tax_number_document.name)
                type, encoding = mimetypes.guess_type(obj.tax_number_document.name)
                response = HttpResponse(file, content_type=type)
                response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                    filename=obj.tax_number_document.name)
                return response
            else:
                file = os.path.join(settings.MEDIA_ROOT, obj.tax_number_document.name)
        raise Http404

    @action(methods=['get'], detail=True)
    def download_registration_number_document(self, request, pk=None):
        """GET download registration number document"""
        try:
            obj = CompanyGeneralDocuments.objects.get(id=pk, user_id=request.user.pk)
        except CompanyGeneralDocuments.DoesNotExist:
            raise Http404

        if obj.registration_number_document.name:
            if STORAGE.exists(name=obj.registration_number_document.name):
                file = STORAGE._read(name=obj.registration_number_document.name)
                type, encoding = mimetypes.guess_type(obj.registration_number_document.name)
                response = HttpResponse(file, content_type=type)
                response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                    filename=obj.registration_number_document.name)
                return response
            else:
                file = os.path.join(settings.MEDIA_ROOT, obj.registration_number_document.name)
        raise Http404

    @action(methods=['get'], detail=True)
    def download_bank_account_document(self, request, pk=None):
        """GET download bank account document"""
        try:
            obj = CompanyGeneralDocuments.objects.get(id=pk, user_id=request.user.pk)
        except CompanyGeneralDocuments.DoesNotExist:
            raise Http404

        if obj.bank_account_document.name:
            if STORAGE.exists(name=obj.bank_account_document.name):
                file = STORAGE._read(name=obj.bank_account_document.name)
                type, encoding = mimetypes.guess_type(obj.bank_account_document.name)
                response = HttpResponse(file, content_type=type)
                response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                    filename=obj.bank_account_document.name)
                return response
            else:
                file = os.path.join(settings.MEDIA_ROOT, obj.bank_account_document.name)
        raise Http404


class AgencyGeneralDocumentsViewSet(viewsets.ModelViewSet):
    serializer_class = AgencyGeneralDocumentsSerializer
    permission_classes = (IsAuthenticated, IsAgency)

    def get_queryset(self):
        user_id = self.request.user.id
        return AgencyGeneralDocuments.objects.filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        """POST create company general documents object"""
        user_id = request.user.id
        if AgencyGeneralDocuments.objects.filter(user_id=user_id).exists():
            return Response(
                {'status': _('You cannot upload data one more time. To change it, please contact us.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """PUT update company general documents object"""
        for field in request.data:
            ChangeFieldValidator.validate(self, field=field)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """PATCH update company general documents object"""
        for field in request.data:
            ChangeFieldValidator.validate(self, field=field)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        response = {"detail": _("You do not have permission to perform this action.")}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get'], detail=True)
    def download_tax_number_document(self, request, pk=None):
        """GET download tax number document"""
        try:
            obj = AgencyGeneralDocuments.objects.get(id=pk, user_id=request.user.pk)
        except AgencyGeneralDocuments.DoesNotExist:
            raise Http404

        if obj.tax_number_document.name:
            if STORAGE.exists(name=obj.tax_number_document.name):
                file = STORAGE._read(name=obj.tax_number_document.name)
                type, encoding = mimetypes.guess_type(obj.tax_number_document.name)
                response = HttpResponse(file, content_type=type)
                response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                    filename=obj.tax_number_document.name)
                return response
            else:
                file = os.path.join(settings.MEDIA_ROOT, obj.tax_number_document.name)
        raise Http404

    @action(methods=['get'], detail=True)
    def download_registration_number_document(self, request, pk=None):
        """GET download registration number document"""
        try:
            obj = AgencyGeneralDocuments.objects.get(id=pk, user_id=request.user.pk)
        except AgencyGeneralDocuments.DoesNotExist:
            raise Http404

        if obj.registration_number_document.name:
            if STORAGE.exists(name=obj.registration_number_document.name):
                file = STORAGE._read(name=obj.registration_number_document.name)
                type, encoding = mimetypes.guess_type(obj.registration_number_document.name)
                response = HttpResponse(file, content_type=type)
                response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                    filename=obj.registration_number_document.name)
                return response
            else:
                file = os.path.join(settings.MEDIA_ROOT, obj.registration_number_document.name)
        raise Http404

    @action(methods=['get'], detail=True)
    def download_bank_account_document(self, request, pk=None):
        """GET download bank account document"""
        try:
            obj = AgencyGeneralDocuments.objects.get(id=pk, user_id=request.user.pk)
        except AgencyGeneralDocuments.DoesNotExist:
            raise Http404

        if obj.bank_account_document.name:
            if STORAGE.exists(name=obj.bank_account_document.name):
                file = STORAGE._read(name=obj.bank_account_document.name)
                type, encoding = mimetypes.guess_type(obj.bank_account_document.name)
                response = HttpResponse(file, content_type=type)
                response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                    filename=obj.bank_account_document.name)
                return response
            else:
                file = os.path.join(settings.MEDIA_ROOT, obj.bank_account_document.name)
        raise Http404


class RetrieveUpdateCandidateGeneralDocumentsView(generics.RetrieveUpdateAPIView):
    serializer_class = RetrieveUpdateCandidateGeneralDocumentsSerializer
    permission_classes = (IsAuthenticated, IsCandidate, IsOwner)

    def get_object(self):
        user_id = self.request.user.id
        return get_object_or_404(CandidateGeneralDocuments, user_id=user_id)

    def put(self, request, *args, **kwargs):
        for field in request.data:
            ChangeFieldValidator.validate(self, field=field)
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        for field in request.data:
            ChangeFieldValidator.validate(self, field=field)
        return super().partial_update(request, *args, **kwargs)


class CandidateGeneralDocumentsViewSet(viewsets.ModelViewSet):
    serializer_class = CandidateGeneralDocumentsSerializer
    permission_classes = (IsAuthenticated, IsCandidate)

    def get_queryset(self):
        user_id = self.request.user.id
        return CandidateGeneralDocuments.objects.filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        user_id = request.user.id
        if CandidateGeneralDocuments.objects.filter(user_id=user_id).exists():
            return Response(
                {'status': _('You cannot upload data one more time. To change it, please contact us.')},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        for field in request.data:
            ChangeFieldValidator.validate(self, field=field)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        for field in request.data:
            ChangeFieldValidator.validate(self, field=field)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        response = {"detail": _("You do not have permission to perform this action.")}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    @action(methods=['get'], detail=True)
    def download_passport_scan(self, request, pk=None):
        """GET download passport scan"""
        try:
            obj = CandidateGeneralDocuments.objects.get(id=pk, user_id=request.user.pk)
        except CandidateGeneralDocuments.DoesNotExist:
            raise Http404

        if obj.passport_scan.name:
            if STORAGE.exists(name=obj.passport_scan.name):
                file = STORAGE._read(name=obj.passport_scan.name)
                type, encoding = mimetypes.guess_type(obj.passport_scan.name)
                response = HttpResponse(file, content_type=type)
                response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                    filename=obj.passport_scan.name)
                return response
            else:
                file = os.path.join(settings.MEDIA_ROOT, obj.passport_scan.name)
        raise Http404

    @action(methods=['get'], detail=True)
    def download_international_passport_scan(self, request, pk=None):
        """GET download international passport scan"""
        try:
            obj = CandidateGeneralDocuments.objects.get(id=pk, user_id=request.user.pk)
        except CandidateGeneralDocuments.DoesNotExist:
            raise Http404

        if obj.international_passport_scan.name:
            if STORAGE.exists(name=obj.international_passport_scan.name):
                file = STORAGE._read(name=obj.international_passport_scan.name)
                type, encoding = mimetypes.guess_type(obj.international_passport_scan.name)
                response = HttpResponse(file, content_type=type)
                response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                    filename=obj.international_passport_scan.name)
                return response
            else:
                file = os.path.join(settings.MEDIA_ROOT, obj.international_passport_scan.name)
        raise Http404

    @action(methods=['get'], detail=True)
    def download_registration_number_document(self, request, pk=None):
        """GET download registration number document"""
        try:
            obj = CandidateGeneralDocuments.objects.get(id=pk, user_id=request.user.pk)
        except CandidateGeneralDocuments.DoesNotExist:
            raise Http404

        if obj.registration_number_document.name:
            if STORAGE.exists(name=obj.registration_number_document.name):
                file = STORAGE._read(name=obj.registration_number_document.name)
                type, encoding = mimetypes.guess_type(obj.registration_number_document.name)
                response = HttpResponse(file, content_type=type)
                response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                    filename=obj.registration_number_document.name)
                return response
            else:
                file = os.path.join(settings.MEDIA_ROOT, obj.registration_number_document.name)
        raise Http404

    @action(methods=['get'], detail=True)
    def download_bank_account_document(self, request, pk=None):
        """GET download bank account document"""
        try:
            obj = CandidateGeneralDocuments.objects.get(id=pk, user_id=request.user.pk)
        except CandidateGeneralDocuments.DoesNotExist:
            raise Http404

        if obj.bank_account_document.name:
            if STORAGE.exists(name=obj.bank_account_document.name):
                file = STORAGE._read(name=obj.bank_account_document.name)
                type, encoding = mimetypes.guess_type(obj.bank_account_document.name)
                response = HttpResponse(file, content_type=type)
                response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                    filename=obj.bank_account_document.name)
                return response
            else:
                file = os.path.join(settings.MEDIA_ROOT, obj.bank_account_document.name)
        raise Http404


class UploadCompanySecureDocumentView(generics.CreateAPIView):
    """
    Endpoint for Company to upload secure documents
    """
    serializer_class = UploadCompanySecureDocumentSerializer
    permission_classes = (IsAuthenticated, IsCompany, IsOwner)


class UploadAgencySecureDocumentView(generics.CreateAPIView):
    """
    Endpoint for Company to upload secure documents
    """
    serializer_class = UploadAgencySecureDocumentSerializer
    permission_classes = (IsAuthenticated, IsAgency, IsOwner)


class UploadCandidateSecureDocumentView(generics.CreateAPIView):
    """
    Endpoint for Company to upload secure documents
    """
    serializer_class = UploadCandidateSecureDocumentSerializer
    permission_classes = (IsAuthenticated, IsCandidate, IsOwner)


class CandidateSecureDocumentViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = CandidateSecureDocumentSerializer
    permission_classes = (IsAuthenticated, IsCandidate, IsOwner)

    def get_queryset(self):
        user_id = self.request.user.id
        return CandidateSecureDocument.objects.filter(user_id=user_id)

    @action(methods=['get'], detail=True)
    def download(self, request, pk=None):
        try:
            obj = CandidateSecureDocument.objects.get(id=pk, user_id=request.user.pk)
        except CandidateSecureDocument.DoesNotExist:
            raise Http404

        if STORAGE.exists(name=obj.secure_document.name):
            file = STORAGE._read(name=obj.secure_document.name)
            type, encoding = mimetypes.guess_type(obj.secure_document.name)
            response = HttpResponse(file, content_type=type)
            response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                filename=obj.secure_document.name)
            return response
        else:
            file = os.path.join(settings.MEDIA_ROOT, obj.secure_document.name)

        raise Http404


class CompanySecureDocumentViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = CompanySecureDocumentSerializer
    permission_classes = (IsAuthenticated, IsCompany, IsOwner)

    def get_queryset(self):
        user_id = self.request.user.id
        return CompanySecureDocument.objects.filter(user_id=user_id)

    @action(methods=['get'], detail=True)
    def download(self, request, pk=None):
        try:
            obj = CompanySecureDocument.objects.get(id=pk, user_id=request.user.pk)
        except CompanySecureDocument.DoesNotExist:
            raise Http404

        if STORAGE.exists(name=obj.secure_document.name):
            file = STORAGE._read(name=obj.secure_document.name)
            type, encoding = mimetypes.guess_type(obj.secure_document.name)
            response = HttpResponse(file, content_type=type)
            response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                filename=obj.secure_document.name)
            return response
        else:
            file = os.path.join(settings.MEDIA_ROOT, obj.secure_document.name)

        raise Http404


class AgencySecureDocumentViewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = AgencySecureDocumentSerializer
    permission_classes = (IsAuthenticated, IsAgency, IsOwner)

    def get_queryset(self):
        user_id = self.request.user.id
        return AgencySecureDocument.objects.filter(user_id=user_id)

    @action(methods=['get'], detail=True)
    def download(self, request, pk=None):
        try:
            obj = AgencySecureDocument.objects.get(id=pk, user_id=request.user.pk)
        except AgencySecureDocument.DoesNotExist:
            raise Http404

        if STORAGE.exists(name=obj.secure_document.name):
            file = STORAGE._read(name=obj.secure_document.name)
            type, encoding = mimetypes.guess_type(obj.secure_document.name)
            response = HttpResponse(file, content_type=type)
            response['Content-Disposition'] = u'attachment; filename="{filename}'.format(
                filename=obj.secure_document.name)
            return response
        else:
            file = os.path.join(settings.MEDIA_ROOT, obj.secure_document.name)

        raise Http404
