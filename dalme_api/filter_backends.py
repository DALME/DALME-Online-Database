from rest_framework.filters import OrderingFilter

from django.db.models import OuterRef, Subquery

from dalme_app.models import Attribute, AttributeType


class DalmeOrderingFilter(OrderingFilter):
    """Ordering filter."""

    def filter_queryset(self, request, queryset, view):
        """Return filtered queryset."""
        ordering = self.get_ordering(request, queryset, view)
        ordering_aggregates = getattr(view, 'ordering_aggregates', [])

        if ordering:
            _ordering = []
            for flt in ordering:
                cf = self.clean_field(flt)
                if cf.startswith('attributes.'):
                    att_type = AttributeType.objects.get(name=cf[11:])
                    attributes = Attribute.objects.filter(object_id=OuterRef('pk'), attribute_type=att_type)
                    if att_type.data_type == 'DATE':
                        queryset = (
                            queryset.annotate(**{cf + '_d': Subquery(attributes.values('value_DATE_d'))})
                            .annotate(**{cf + '_m': Subquery(attributes.values('value_DATE_m'))})
                            .annotate(**{cf + '_y': Subquery(attributes.values('value_DATE_y'))})
                        )
                        _ordering += [f'{flt}_y', f'{flt}_m', f'{flt}_d']

                    else:
                        queryset = queryset.annotate(**{cf: Subquery(attributes.values('value_STR'))})
                        _ordering.append(flt)

                elif cf in ordering_aggregates:
                    queryset = queryset.annotate(**self.get_annotation(cf, ordering_aggregates[cf]))
                    _ordering.append(f'{flt}_a')

                else:
                    _ordering.append(flt)

            return queryset.order_by(*_ordering)

        return queryset

    @staticmethod
    def get_annotation(key, para):
        """Return annotation expression."""
        return {f'{key}_a': eval(f"{para['function']}('{para['expression']}')")}  # noqa: PGH001

    @staticmethod
    def clean_field(field):
        """Return clean field."""
        return field[1:] if field.startswith('-') else field
