"""Filter for ordering records."""

import django_filters

from django.db.models import OuterRef, Q, Subquery

from ida.models import Attribute


class RecordOrderingFilter(django_filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('name', 'Name'),
            ('-name', 'Name (descending)'),
            ('record_type', 'Type'),
            ('-recordtype', 'Type (descending)'),
            ('date', 'Date'),
            ('-date', 'Date (descending)'),
        ]

    @staticmethod
    def get_value(field, value):
        if not value:
            return False
        return next((v for v in value if v and v.endswith(field)), False)

    @staticmethod
    def annotate_dates(qs):
        dates = Attribute.objects.filter(
            Q(records=OuterRef('pk'), attribute_type__name='date')
            | Q(records=OuterRef('pk'), attribute_type__name='start_date')
            | Q(records=OuterRef('pk'), attribute_type__name='end_date'),
        )
        qs = qs.annotate(record_date=Subquery(dates.values('attributevaluedate__year')[:1]))
        return qs.distinct()

    @staticmethod
    def annotate_record_type(qs):
        record_types = Attribute.objects.filter(
            records=OuterRef('pk'),
            attribute_type__name='record_type',
        )
        return qs.annotate(
            record_type=Subquery(record_types.values('attributevaluestr__value')[:1]),
        ).distinct()

    def filter(self, qs, value):
        qs = super().filter(qs, value=[])
        # For now any duplicates that remain here after filtering are
        # eliminated on the endpoint itself before going down the wire.
        # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#distinct
        date = self.get_value('date', value)
        if date:
            self.parent.annotated = True
            qs = self.annotate_dates(qs)

        record_type = self.get_value('record_type', value)
        if record_type:
            self.parent.annotated = True
            qs = self.annotate_record_type(qs)

        name = self.get_value('name', value)
        if name:
            qs = qs.order_by(name)

        return qs
