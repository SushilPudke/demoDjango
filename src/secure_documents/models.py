import os

from django.db import models
from django.core.validators import FileExtensionValidator

from .constants import SECURE_DOCUMENT_TYPE
from base.models import TimeStampedUUIDModel

from storages.backends.sftpstorage import SFTPStorage


STORAGE = SFTPStorage()


def agencies_directory_path(instance, filename):
    return f'agencies_secure_document/{instance.user_id}/{filename}'


def companies_directory_path(instance, filename):
    return f'companies_secure_document/{instance.user_id}/{filename}'


def candidates_directory_path(instance, filename):
    return f'candidates_secure_document/{instance.user_id}/{filename}'


class CompanySecureDocument(TimeStampedUUIDModel):
    user_id = models.IntegerField()
    document_type = models.IntegerField(choices=SECURE_DOCUMENT_TYPE)
    secure_document = models.FileField(
        upload_to=companies_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx'])]
    )

    def __str__(self):
        secure_document = os.path.basename(self.secure_document.file.name)
        return f'{self.user_id}_<{secure_document}>'


class CompanyGeneralDocuments(TimeStampedUUIDModel):
    user_id = models.IntegerField()
    tax_number = models.CharField(max_length=50, blank=True)
    tax_number_document = models.FileField(
        blank=True,
        upload_to=companies_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls',
                                                               'xlsx', 'png', 'jpg', 'jpeg'])]
    )
    registration_number = models.CharField(max_length=50, blank=True)
    registration_number_document = models.FileField(
        blank=True,
        upload_to=companies_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls',
                                                               'xlsx', 'png', 'jpg', 'jpeg'])]
    )
    is_sepa_region = models.BooleanField(default=True)
    iban_code = models.CharField(max_length=50, blank=True)
    bank_account_document = models.FileField(
        blank=True,
        upload_to=companies_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls',
                                                               'xlsx', 'png', 'jpg', 'jpeg'])]
    )

    def __str__(self):
        return f'{self.user_id}_<General Documents>'


class AgencySecureDocument(TimeStampedUUIDModel):
    user_id = models.IntegerField()
    document_type = models.IntegerField(choices=SECURE_DOCUMENT_TYPE)
    secure_document = models.FileField(
        upload_to=agencies_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx'])]
    )

    def __str__(self):
        secure_document = os.path.basename(self.secure_document.file.name)
        return f'{self.user_id}_<{secure_document}>'


class AgencyGeneralDocuments(TimeStampedUUIDModel):
    user_id = models.IntegerField()
    tax_number = models.CharField(max_length=50, blank=True)
    tax_number_document = models.FileField(
        blank=True,
        upload_to=agencies_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls',
                                                               'xlsx', 'png', 'jpg', 'jpeg'])]
    )
    registration_number = models.CharField(max_length=50, blank=True)
    registration_number_document = models.FileField(
        blank=True,
        upload_to=agencies_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls',
                                                               'xlsx', 'png', 'jpg', 'jpeg'])]
    )
    is_sepa_region = models.BooleanField(default=True)
    iban_code = models.CharField(max_length=50, blank=True)
    bank_account_document = models.FileField(
        blank=True,
        upload_to=agencies_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls',
                                                               'xlsx', 'png', 'jpg', 'jpeg'])]
    )

    def __str__(self):
        return f'{self.user_id}_<General Documents>'


class CandidateSecureDocument(TimeStampedUUIDModel):
    user_id = models.IntegerField()
    document_type = models.IntegerField(choices=SECURE_DOCUMENT_TYPE)
    secure_document = models.FileField(
        upload_to=candidates_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls', 'xlsx'])]
    )

    def __str__(self):
        secure_document = os.path.basename(self.secure_document.file.name)
        return f'{self.user_id}_<{secure_document}>'


class CandidateGeneralDocuments(TimeStampedUUIDModel):
    user_id = models.IntegerField()
    passport_scan = models.FileField(
        blank=True,
        upload_to=candidates_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls',
                                                               'xlsx', 'png', 'jpg', 'jpeg'])]
        )
    international_passport_scan = models.FileField(
        blank=True,
        upload_to=candidates_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls',
                                                               'xlsx', 'png', 'jpg', 'jpeg'])]
        )
    registration_number = models.CharField(max_length=50, blank=True)
    registration_number_document = models.FileField(
        blank=True,
        upload_to=candidates_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls',
                                                               'xlsx', 'png', 'jpg', 'jpeg'])]
        )
    is_sepa_region = models.BooleanField(default=True)
    iban_code = models.CharField(max_length=50, blank=True)
    bank_account_document = models.FileField(
        blank=True,
        upload_to=candidates_directory_path,
        storage=STORAGE,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'xls',
                                                               'xlsx', 'png', 'jpg', 'jpeg'])]
        )

    def __str__(self):
        return f'{self.user_id}_<General Documents>'
