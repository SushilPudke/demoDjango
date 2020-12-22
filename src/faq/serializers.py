from rest_framework import serializers

from django.utils.translation import ugettext_lazy as _

from .models import Question


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = (
            'id',
            'question_headline',
            'answer',
            'question_type'
        )


class ContactFormSerializer(serializers.Serializer):
    full_name = serializers.CharField(
        max_length=255,
        required=True,
        error_messages={
            "max_length": _("Please enter maximum 255 symbols"),
            "blank": _("This field is required")
        }
    )
    email = serializers.EmailField(
        max_length=255,
        required=True,
        error_messages={
            "max_length": _("Please enter maximum 255 symbols"),
            "invalid": _("Not valid email address"),
            "blank": _("This field is required")
        }
    )
    question = serializers.CharField(
        required=True,
        error_messages={
            "blank": _("This field is required")
        }
    )
