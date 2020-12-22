from modeltranslation.translator import register, TranslationOptions
from .models import Question


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = (
        'question_headline',
        'answer',
    )
