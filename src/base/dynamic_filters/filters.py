from copy import deepcopy
from typing import List

from django.db.models import Count, Q
from django_filters import filters as _filters
from django.utils.translation import ugettext_lazy as _

__all__ = [
    'DynamicFilter',
    'ModelChoiceFilter',
    'ModelMultipleChoiceFilter',
    'MultipleChoiceFilter',
    'ChoiceFilter',
]


def remove_clause(queryset, lookup):
    queryset = deepcopy(queryset)

    query = queryset.query
    q = Q(**{lookup: None})
    clause, _ = query._add_q(q, query.used_aliases)

    def filter_lookups(child):
        if hasattr(child, 'lhs'):
            return child.lhs.target != clause.children[0].lhs.target

        return len(list(filter(filter_lookups, child.children))) == len(child.children)

    query.where.children = list(filter(filter_lookups, query.where.children))

    return queryset


class DynamicFilter(_filters.Filter):
    def __init__(self, *args, only_stats=False, **kwargs):
        # Display only stats without actual filtering
        # Used for displaying dynamic filters stats
        self.only_stats = only_stats

        super().__init__(*args, **kwargs)

    def get_options(self) -> List[tuple]:
        return self.extra['choices']

    def get_group_queryset(self, queryset) -> List[tuple]:
        return queryset.values(self.field_name) \
            .annotate(total=Count(self.field_name)) \
            .order_by('total') \
            .values_list(self.field_name, 'total')

    def get_option_stats(self, queryset):
        if self.only_stats:
            queryset = self.parent.queryset
        else:
            queryset = remove_clause(queryset, self.field_name)

        stats = self.get_group_queryset(queryset)

        stats_dict = {str(pk): total for pk, total in stats}
        stats = []

        for pk, label in self.get_options():
            stats.append(
                {
                    'value': pk,
                    'label': str(_(label)),
                    'count': stats_dict.get(str(pk)) or None
                }
            )

        return stats


class QuerySetRequestMixin(_filters.QuerySetRequestMixin):
    def get_options(self) -> List[tuple]:
        return [
            (o.pk, str(o)) for o in self.queryset
        ]


class ModelChoiceFilter(QuerySetRequestMixin, DynamicFilter, _filters.ModelChoiceFilter):
    pass


class ModelMultipleChoiceFilter(QuerySetRequestMixin, DynamicFilter, _filters.ModelMultipleChoiceFilter):
    pass


class MultipleChoiceFilter(DynamicFilter, _filters.MultipleChoiceFilter):
    """
    Multiply filters of multiply choices field (str A, B, C)
    """

    def get_group_queryset(self, queryset) -> List[tuple]:
        if self.lookup_expr == 'contains':
            option_ids = list(zip(*self.get_options()))[0]

            queryset = queryset.aggregate(**{
                str(o): Count(self.field_name, filter=Q(**{
                    '{}__{}'.format(self.field_name, self.lookup_expr): o
                }))
                for o in option_ids
            })

            return list(queryset.items())

        return super().get_group_queryset(queryset)


class ChoiceFilter(DynamicFilter, _filters.ChoiceFilter):
    pass
