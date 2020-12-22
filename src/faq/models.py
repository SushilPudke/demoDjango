from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import TimeStampedModel


class Question(TimeStampedModel):
    QUESTION_TYPE = (
        ('COMPANY', _('For company')),
        ('CANDIDATE', _('For candidate')),
        ('AGENCY', _('For agencies')),
    )
    question_headline = models.CharField(_('Question headline'), max_length=255)
    answer = models.TextField(_('Answer'))
    question_type = models.CharField(_('Question type'), choices=QUESTION_TYPE, max_length=32)

    def __str__(self):
        return self.question_headline
