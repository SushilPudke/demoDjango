from copy import deepcopy

from django.db import models
from django.db.models.fields.related import (
    ManyToManyRel,
    ManyToOneRel,
    OneToOneRel
)
from django.utils.translation import ugettext_lazy as _
from django_filters import filterset
from django_filters.rest_framework import FilterSet

from base.dynamic_filters.filters import (
    DynamicFilter,
    ModelChoiceFilter,
    ModelMultipleChoiceFilter,
)


FILTER_FOR_DBFIELD_DEFAULTS = deepcopy(filterset.FILTER_FOR_DBFIELD_DEFAULTS)

NEW_FILTERS = {
    models.OneToOneField: {'filter_class': ModelChoiceFilter},
    models.ForeignKey: {'filter_class': ModelChoiceFilter},
    models.ManyToManyField: {'filter_class': ModelMultipleChoiceFilter},
    # Reverse relationships
    OneToOneRel: {'filter_class': ModelChoiceFilter},
    ManyToOneRel: {'filter_class': ModelMultipleChoiceFilter},
    ManyToManyRel: {'filter_class': ModelMultipleChoiceFilter},
}

for name, value in NEW_FILTERS.items():
    FILTER_FOR_DBFIELD_DEFAULTS[name].update(value)


class DynamicFilterSet(FilterSet):
    FILTER_DEFAULTS = FILTER_FOR_DBFIELD_DEFAULTS

    def get_dynamic_filters_set(self, queryset):
        filters_list = []

        for field in self.filters.values():
            if not isinstance(field, DynamicFilter):
                continue

            filters_list.append(
                {
                    'name': str(_(field.label)),
                    'filter_type': field.field_name,
                    'items': field.get_option_stats(queryset)
                }
            )

        return filters_list
