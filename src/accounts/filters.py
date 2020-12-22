from django.utils.translation import ugettext_lazy as _

from accounts.models import Specialization, Technology
from base import dynamic_filters
from base.languages.constants import COUNTRY_CHOICES

from .models import EXPERIENCE, EXPERIENCE_LVL, JOB_TYPE, AgencyProfile, CandidateProfile


class CandidateFilter(dynamic_filters.DynamicFilterSet):
    specialization = dynamic_filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        label=_('Category')
    )
    technologies = dynamic_filters.ModelMultipleChoiceFilter(
        queryset=Technology.objects.all().order_by('technology_name'),
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
        choices=COUNTRY_CHOICES
    )

    class Meta:
        model = CandidateProfile
        fields = []


class CandidateFilterStats(CandidateFilter):
    specialization = dynamic_filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        label=_('Category'),
        only_stats=True,
    )


class AgencyFilter(dynamic_filters.DynamicFilterSet):
    specialization = dynamic_filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        label=_('Category')
    )
    technologies = dynamic_filters.ModelMultipleChoiceFilter(
        queryset=Technology.objects.all().order_by('technology_name'),
        label=_('Skills')
    )
    country = dynamic_filters.MultipleChoiceFilter(
        label=_('Country'),
        choices=COUNTRY_CHOICES
    )

    class Meta:
        model = AgencyProfile
        fields = []


class AgencyFilterStats(AgencyFilter):
    specialization = dynamic_filters.ModelMultipleChoiceFilter(
        queryset=Specialization.objects.all(),
        label=_('Category'),
        only_stats=True,
    )
