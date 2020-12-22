from django_filters.rest_framework.backends import DjangoFilterBackend, utils


class DynamicDjangoFilterBackend(DjangoFilterBackend):
    def __init__(self, filterset_class=None):
        self.filterset_class = filterset_class

    def get_filterset_class(self, view, queryset=None):
        if self.filterset_class:
            filterset_model = self.filterset_class._meta.model

            # FilterSets do not need to specify a Meta class
            if filterset_model and queryset is not None:
                assert issubclass(queryset.model, filterset_model), \
                    'FilterSet model %s does not match queryset model %s' % \
                    (filterset_model, queryset.model)

            return self.filterset_class

        return super().get_filterset_class(view, queryset)

    def get_dynamic_filters(self, request, queryset, view):
        filterset = self.get_filterset(request, queryset, view)
        if filterset is None:
            return queryset

        if not filterset.is_valid() and self.raise_exception:
            raise utils.translate_validation(filterset.errors)

        return filterset.get_dynamic_filters_set(filterset.qs)
