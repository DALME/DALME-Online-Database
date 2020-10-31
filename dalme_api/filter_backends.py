from rest_framework.filters import OrderingFilter
from django.db.models import Count, OuterRef, Subquery
from dalme_app.models import Attribute, Attribute_type


class DalmeOrderingFilter(OrderingFilter):

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        ordering_aggregates = getattr(view, 'ordering_aggregates', [])

        if ordering:
            _ordering = []
            for f in ordering:
                cf = self.clean_field(f)
                if cf.startswith('attributes.'):
                    type = Attribute_type.objects.get(short_name=cf[11:])
                    attributes = Attribute.objects.filter(object_id=OuterRef('pk'), attribute_type=type)
                    if type.data_type == 'DATE':
                        queryset = queryset.annotate(
                            **{cf + '_d': Subquery(attributes.values('value_DATE_d'))}
                        ).annotate(
                            **{cf + '_m': Subquery(attributes.values('value_DATE_m'))}
                        ).annotate(
                            **{cf + '_y': Subquery(attributes.values('value_DATE_y'))}
                        )
                        _ordering += [f + '_y', f + '_m', f + '_d']
                    else:
                        queryset = queryset.annotate(**{cf: Subquery(attributes.values('value_STR'))})
                        _ordering.append(f)
                elif cf in ordering_aggregates:
                    queryset = queryset.annotate(**self.get_annotation(cf, ordering_aggregates[cf]))
                    _ordering.append(f + '_a')
                else:
                    _ordering.append(f)

            return queryset.order_by(*_ordering)

        return queryset

    @staticmethod
    def get_annotation(key, para):
        return {key + '_a': eval(para['function'] + '(\'' + para['expression'] + '\')')}

    @staticmethod
    def clean_field(field):
        if field.startswith('-'):
            field = field[1:]
        return field
