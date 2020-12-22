from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import (Project, Position, PositionDocument, ProjectDocument,
                     CandidatePositionApplication, AgencyPositionApplication)


class ProjectResource(resources.ModelResource):

    class Meta:
        model = Project
        import_id_fields = ('id',)
        fields = (
            'id',
            'project_name',
            'project_name_de',
            'project_description',
            'project_description_de',
            'location',
            'location_de',
            'company',
        )


class PositionResource(resources.ModelResource):

    class Meta:
        model = Position
        import_id_fields = ('id',)
        exclude = (
            'created',
            'modified',
            'salary',
            'offers_en',
            'requirements_en',
            'position_title_en'
        )


@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    raw_id_fields = ('company',)
    search_fields = ('project_name',)
    list_display = ('project_name', 'id', 'company', 'company_id', 'created')
    resource_class = ProjectResource
    exclude = (
        'project_name_en',
        'project_description_en',
        'location_en'
    )


@admin.register(Position)
class PositionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    raw_id_fields = ('company', 'project')
    search_fields = ('position_title',)
    list_display = ('position_title', 'id', 'project', 'project_id', 'company', 'company_id', 'created')
    resource_class = PositionResource
    exclude = (
        'position_title_en',
        'requirements_en',
        'offers_en'
    )


@admin.register(PositionDocument)
class PositionDocumentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'company', 'company_id', 'created')


@admin.register(ProjectDocument)
class ProjectDocumentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'id', 'company', 'company_id', 'created')


@admin.register(CandidatePositionApplication)
class CandidatePositionApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'position', 'created')


@admin.register(AgencyPositionApplication)
class AgencyPositionApplicationAdmin(admin.ModelAdmin):
    list_display = ('agency', 'position', 'created')
