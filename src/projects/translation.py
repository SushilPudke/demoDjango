from modeltranslation.translator import register, TranslationOptions
from .models import Project, Position


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = (
        'project_name',
        'project_description',
        'location'
    )


@register(Position)
class PositionTranslationOptions(TranslationOptions):
    fields = (
        'position_title',
        'requirements',
        'offers'
    )
