from django.contrib import admin

from .models import Question

from import_export import resources
from import_export.admin import ImportExportModelAdmin


class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question
        import_id_fields = ('id',)
        exclude = (
            'created',
            'modified',
            'question_headline_en',
            'answer_en'
        )


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('question_headline', 'question_type')
    search_fields = ('question_headline',)
    list_filter = ('question_type',)
    resource_class = QuestionResource
