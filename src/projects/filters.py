from django.utils.translation import ugettext_lazy as _

from base import dynamic_filters
from base.languages.constants import COUNTRY_AVAILABLE_CHOICES
from accounts.models import Specialization, Technology
from .models import (
    Position,
    JOB_TYPE,
    EXPERIENCE,
    EXPERIENCE_LVL,
)


class PositionFilter(dynamic_filters.DynamicFilterSet):
    specialization = dynamic_filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        label=_('Category')
    )
    technologies = dynamic_filters.ModelMultipleChoiceFilter(
        queryset=Technology.objects.all(),
        label=_('Skills')
    )
    job_type = dynamic_filters.MultipleChoiceFilter(
        label=_('Job type'),
        choices=JOB_TYPE, lookup_expr='contains'
    )
    experience = dynamic_filters.MultipleChoiceFilter(
        choices=EXPERIENCE
    )
    experience_level = dynamic_filters.MultipleChoiceFilter(
        choices=EXPERIENCE_LVL
    )
    country = dynamic_filters.MultipleChoiceFilter(
        label=_('Country'),
        choices=COUNTRY_AVAILABLE_CHOICES
    )

    class Meta:
        model = Position
        fields = []


class PositionFilterStats(PositionFilter):
    specialization = dynamic_filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        label=_('Category'),
        only_stats=True
    )
