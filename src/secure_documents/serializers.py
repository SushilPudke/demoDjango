import os.path

from rest_framework import serializers
from django.db import models
from rest_framework.validators import ValidationError
from django.utils.translation import ugettext_lazy as _

from accounts.validators import FileSizeValidator

from .models import (CompanySecureDocument, CompanyGeneralDocuments,
                     CandidateGeneralDocuments, CandidateSecureDocument,
                     AgencyGeneralDocuments, AgencySecureDocument)
from .validators import ChangeFieldValidator


class FileField(serializers.FileField):
    def to_representation(self, value):
        try:
            url = value.url
        except (AttributeError, ValueError):
            return None

        return os.path.basename(url)


class CustomModelSerializer(serializers.ModelSerializer):
    serializer_field_mapping = {
        **serializers.ModelSerializer.serializer_field_mapping,
        **{models.FileField: FileField}
    }


class CandidateGeneralDocumentsSerializer(CustomModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CandidateGeneralDocuments
        fields = '__all__'

    def validate_passport_scan(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def validate_international_passport_scan(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def validate_registration_number_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def validate_bank_account_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def validate(self, data):
        is_sepa_region = data.get('is_sepa_region')
        iban_code = data.get('iban_code')
        bank_account_document = data.get('bank_account_document')

        if bank_account_document and is_sepa_region:
            raise ValidationError({
                "bank_account_document": _("Please, provide IBAN code or choose Non-SEPA region"),
                "is_sepa_region": _("Please, provide IBAN code or choose Non-SEPA region")
            })

        if iban_code and bank_account_document:
            raise ValidationError({
                "iban_code": _("Please provide either a number or upload a file"),
                "bank_account_document": _("Please provide either a number or upload a file"),
            })

        return super(CandidateGeneralDocumentsSerializer, self).validate(data)

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        return CandidateGeneralDocuments.objects.create(user_id=user_id, **validated_data)


class CompanyGeneralDocumentsSerializer(CustomModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CompanyGeneralDocuments
        fields = '__all__'

    def validate_tax_number_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def validate_registration_number_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def validate_bank_account_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def validate(self, data):
        is_sepa_region = data.get('is_sepa_region')
        iban_code = data.get('iban_code')
        bank_account_document = data.get('bank_account_document')

        if bank_account_document and is_sepa_region:
            raise ValidationError({"bank_account_document": _("Please, provide bank account details first.")})

        if iban_code and bank_account_document:
            raise ValidationError({
                "iban_code": _("Please provide either a number or upload a file"),
                "bank_account_document": _("Please provide either a number or upload a file"),
            })

        return super(CompanyGeneralDocumentsSerializer, self).validate(data)

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        return CompanyGeneralDocuments.objects.create(user_id=user_id, **validated_data)


class AgencyGeneralDocumentsSerializer(CustomModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CompanyGeneralDocuments
        fields = '__all__'

    def validate_tax_number_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def validate_registration_number_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def validate_bank_account_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def validate(self, data):
        is_sepa_region = data.get('is_sepa_region')
        iban_code = data.get('iban_code')
        bank_account_document = data.get('bank_account_document')

        if bank_account_document and is_sepa_region:
            raise ValidationError({"bank_account_document": _("Please, provide bank account details first.")})

        if iban_code and bank_account_document:
            raise ValidationError({
                "iban_code": _("Please provide either a number or upload a file"),
                "bank_account_document": _("Please provide either a number or upload a file"),
            })

        return super(AgencyGeneralDocumentsSerializer, self).validate(data)

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        return AgencyGeneralDocuments.objects.create(user_id=user_id, **validated_data)


class RetrieveUpdateCompanyGeneralDocumentsSerializer(CustomModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CompanyGeneralDocuments
        fields = '__all__'

    def validate_tax_number_document(self, value):
        FileSizeValidator.validate(self, file=value)
        ChangeFieldValidator(self, field=value)
        return value

    def validate_registration_number_document(self, value):
        FileSizeValidator.validate(self, file=value)
        ChangeFieldValidator(self, field=value)
        return value

    def validate_bank_account_document(self, value):
        FileSizeValidator.validate(self, file=value)
        ChangeFieldValidator(self, field=value)
        return value


class RetrieveUpdateCandidateGeneralDocumentsSerializer(CustomModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CandidateGeneralDocuments
        fields = '__all__'

    def validate_tax_number_document(self, value):
        FileSizeValidator.validate(self, file=value)
        ChangeFieldValidator(self, field=value)
        return value

    def validate_registration_number_document(self, value):
        FileSizeValidator.validate(self, file=value)
        ChangeFieldValidator(self, field=value)
        return value

    def validate_bank_account_document(self, value):
        FileSizeValidator.validate(self, file=value)
        ChangeFieldValidator(self, field=value)
        return value


class UploadCompanySecureDocumentSerializer(CustomModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CompanySecureDocument
        fields = '__all__'

    def validate_secure_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        return CompanySecureDocument.objects.create(user_id=user_id, **validated_data)


class UploadAgencySecureDocumentSerializer(CustomModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = AgencySecureDocument
        fields = '__all__'

    def validate_secure_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        return AgencySecureDocument.objects.create(user_id=user_id, **validated_data)


class UploadCandidateSecureDocumentSerializer(CustomModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CandidateSecureDocument
        fields = '__all__'

    def validate_secure_document(self, value):
        FileSizeValidator.validate(self, file=value)
        return value

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        return CandidateSecureDocument.objects.create(user_id=user_id, **validated_data)


class CompanySecureDocumentSerializer(CustomModelSerializer):
    class Meta:
        model = CompanySecureDocument
        fields = '__all__'


class AgencySecureDocumentSerializer(CustomModelSerializer):
    class Meta:
        model = AgencySecureDocument
        fields = '__all__'


class CandidateSecureDocumentSerializer(CustomModelSerializer):
    class Meta:
        model = CandidateSecureDocument
        fields = '__all__'
