"""Interface for the ida.filters.utils module."""

import django_filters as filters

from django.contrib.contenttypes.models import ContentType


class BaseAttributeFilter(filters.FilterSet):
    """Base class for filtersets in models with attributes."""

    @property
    def qs(self):
        qs = self.queryset.all()
        ct = ContentType.objects.get_for_model(qs.model)
        if hasattr(ct, 'contenttypeextended'):
            model_fields = [i.name for i in qs.model._meta.get_fields()]  # noqa: SLF001
            attribute_list = [
                i
                for i in ct.contenttypeextended.attribute_types.all().values_list('name', flat=True)
                if i not in model_fields
            ]
            qs = qs.include_attrs(*attribute_list)

        if self.is_bound:
            self.errors  # ensure form validation before filtering  # noqa: B018
            qs = self.filter_queryset(qs)

        self._qs = qs
        return self._qs
