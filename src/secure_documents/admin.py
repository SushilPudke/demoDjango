from django.contrib import admin

from .models import (CompanySecureDocument, CompanyGeneralDocuments,
                     CandidateGeneralDocuments, CandidateSecureDocument,
                     AgencySecureDocument, AgencyGeneralDocuments)


@admin.register(CompanyGeneralDocuments)
class CompanyGeneralDocumentsAdmin(admin.ModelAdmin):
    pass


@admin.register(AgencyGeneralDocuments)
class AgencyGeneralDocumentsAdmin(admin.ModelAdmin):
    pass


@admin.register(CandidateGeneralDocuments)
class CandidateGeneralDocumentsAdmin(admin.ModelAdmin):
    pass


@admin.register(CandidateSecureDocument)
class CandidateSecureDocumentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user_id', 'created', 'modified')


@admin.register(CompanySecureDocument)
class CompanySecureDocumentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user_id', 'created', 'modified')


@admin.register(AgencySecureDocument)
class AgencySecureDocumentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user_id', 'created', 'modified')
