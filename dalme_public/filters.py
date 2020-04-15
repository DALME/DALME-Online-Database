import copy
from datetime import datetime

from django import forms
from django.db.models import Case, F, Q, When
from django.forms.widgets import NullBooleanSelect

import django_filters

from dalme_app.models import Attribute, Source
from dalme_public.models import Collection, Set


DATERANGE_FORMATS = ('%Y', '%b-%Y', '%d-%b-%Y',)
BOOLEAN_CHOICES = [('', '---------'), ('true', 'Yes'), ('false', 'No')]


def _map_source_types():
    # We have to filter over 'value_STR' rather than, say, 'pk' because of the
    # sideways denormalization scheme: there is no unique, one-to-one mapping
    # between Attributes with the same 'value_STR'. Compare:
    #
    #     attrs = Attribute.objects.filter(
    #         attribute_type__short_name='record_type'
    #     )
    #     set([x.value_STR for x in attrs])
    #     set([(x.pk, x.value_STR) for x in attrs])
    #
    # So, let's eliminate the duplicates and index the choices first before
    # sorting them for the frontend widget, that way we can reaccess them by
    # index later to get the right names back when a request with a query comes
    # in. See the `filter_type` method below.
    return {
        str(idx): attr['value_STR']
        for idx, attr in enumerate(Attribute.objects.filter(
            attribute_type__short_name='record_type'
        ).values('value_STR').distinct())
    }

def _collection_choices():
    return [
        (collection.pk, collection.name)
        for collection in Collection.objects.all().order_by('name')
    ]


def _dataset_choices():
    return [
        (dataset.pk, dataset.name)
        for dataset in Set.objects.all().order_by('name')
    ]


def _source_type_choices():
    type_map = _map_source_types()
    return sorted(list(type_map.items()), key=lambda choice: choice[1])


class CustomDateRangeField(django_filters.fields.DateRangeField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            field.input_formats = [DATERANGE_FORMATS]


class CustomDateFromToRangeFilter(django_filters.DateFromToRangeFilter):
    field_class = CustomDateRangeField


class SourceOrderingFilter(django_filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('source_type', 'Type'),
            ('-source_type', 'Type (descending)'),
            ('date', 'Date'),
            ('-date', 'Date (descending)'),
        ]

    @staticmethod
    def get_value(field, value):
        if not value:
            return False
        return next((v for v in value if v and v.endswith(field)), False)

    @staticmethod
    def annotate_dates(queryset):
        return queryset.annotate(
            start_date=Case(
                When(
                    attributes__attribute_type__short_name='start_date',
                    then=F('attributes__value_DATE')
                ),
                default=None
            )
        ).annotate(
            end_date=Case(
                When(
                    attributes__attribute_type__short_name='end_date',
                    then=F('attributes__value_DATE')
                ),
                default=None
            )
        ).distinct()

    def filter(self, qs, value):
        qs = super().filter(qs, value)

        # TODO: Still looking for a solution to the 'distinct' issue.
        # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#distinct
        # Perhaps, as long as we filter for these annotated object last, we can
        # cast the results to `values` and the distinct comparison will
        # succeed. In any case, for now any duplicates that remain here are
        # eliminated on the view itself before template render time.
        date = self.get_value('date', value)
        if date:
            self.parent.annotated = True
            # TODO: It's not perfect, but probably as good as we are going
            # to get without going deep into date data normalization.
            qs = self.annotate_dates(qs)
            if not date.startswith('-'):
                qs = qs.order_by(
                    F('start_date').asc(nulls_last=True),
                    F('end_date').asc(nulls_last=True),
                )
            else:
                qs = qs.order_by(
                    F('start_date').desc(nulls_first=True),
                    F('end_date').desc(nulls_last=True)
                )

        source_type = self.get_value('source_type', value)
        if source_type:
            self.parent.annotated = True
            qs = qs.annotate(
                source_type=Case(
                    When(
                        attributes__attribute_type__short_name='record_type',
                        then=F('attributes__value_STR')
                    ),
                    default=None
                )
            ).distinct()
            if not source_type.startswith('-'):
                qs = qs.order_by(F('source_type').asc(nulls_last=True))
            else:
                qs = qs.order_by(F('source_type').desc(nulls_first=True))

        return qs


class SourceFilterForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()

        self.errors['date_range'] = self.error_class()
        cleaned_data['date_range'] = {}
        date_keys = ['date_range_after', 'date_range_before']
        if any(key in self.data.keys() for key in date_keys):
            for date_key in date_keys:
                if self.data.get(date_key):
                    date = None
                    for fmt in DATERANGE_FORMATS:
                        value = self.data[date_key]
                        try:
                            date = datetime.strptime(value, fmt)
                        except ValueError:
                            continue
                    if not date:
                        # "Note that Form.add_error() automatically removes
                        # the relevant field from cleaned_data."
                        date_range = cleaned_data.pop('date_range')
                        self.add_error(
                            'date_range', f'{value} is not a valid date.'
                        )
                        cleaned_data['date_range'] = date_range
                    else:
                        cleaned_data['date_range'][date_key] = date

            after = cleaned_data['date_range'].get('date_range_after')
            before = cleaned_data['date_range'].get('date_range_before')
            if (after and before) and after > before:
                self.add_error(
                    'date_range',
                    f'The "after" value cannot be greater than the "before" value.'
                )

        return cleaned_data


class SourceFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.annotated = False
        super().__init__(*args, **kwargs)
        for definition in self.filters.values():
            definition.field.label_suffix = ''
            if isinstance(definition.field.widget, NullBooleanSelect):
                definition.field.widget.choices = BOOLEAN_CHOICES

    name = django_filters.CharFilter(label='Name', lookup_expr='icontains')
    source_type = django_filters.MultipleChoiceFilter(
        label='Type',
        choices=_source_type_choices,
        method='filter_type'
    )
    date_range = CustomDateFromToRangeFilter(
        label='Date Range',
        widget=django_filters.widgets.DateRangeWidget(
            attrs={'placeholder': '%Y or %b-%Y or %d-%b-%Y'}
        ),
        method='filter_date_range'
    )
    collection = django_filters.ChoiceFilter(
        label='Collection',
        choices=_collection_choices,
        method='filter_collection'
    )
    dataset = django_filters.ChoiceFilter(
        label='Set',
        choices=_dataset_choices,
        method='filter_dataset'
    )
    has_image = django_filters.BooleanFilter(
        label='Has Image', method='filter_image'
    )
    has_transcription = django_filters.BooleanFilter(
        label='Has Transcription', method='filter_transcription'
    )

    order_by = SourceOrderingFilter(
        fields=(('name', 'name'),)
    )

    class Meta:
        model = Source
        form = SourceFilterForm
        fields = [
            'name',
            'source_type',
            'date_range',
            'collection',
            'dataset',
            'has_transcription',
            'has_image',
            'order_by',
        ]

    def filter_type(self, queryset, name, value):
        # Now we can re-use the type map when a request comes in for filtering.
        type_map = _map_source_types()
        source_types = []
        for idx in value:
            try:
                source_types.append(type_map[idx])
            except KeyError:
                continue
        return queryset.filter(**{'attributes__value_STR__in': source_types})

    def filter_date_range(self, queryset, name, value):
        queryset = queryset.filter(
            attributes__attribute_type__short_name__endswith='_date'
        ).distinct()

        after = value.get('date_range_after')
        before = value.get('date_range_before')
        if after:
            queryset = queryset.filter(attributes__value_DATE__gte=after)
        if before:
            queryset = queryset.filter( attributes__value_DATE__lte=before)

        return queryset

    def filter_collection(self, queryset, name, value):
        try:
            collection = Collection.objects.get(pk=value)
        except Collection.DoesNotExist:
            return queryset.none()
        return queryset.filter(
            sets__set_id__in=[
                dataset.source_set.pk
                for dataset in collection.sets.all()
            ]
        )

    def filter_dataset(self, queryset, name, value):
        try:
            dataset = Set.objects.get(pk=value)
        except Set.DoesNotExist:
            return queryset.none()
        return queryset.filter(sets__set_id=dataset.source_set.pk)

    def filter_image(self, queryset, name, value):
        return queryset.exclude(source_pages__page__dam_id__isnull=value)

    def filter_transcription(self, queryset, name, value):
        return queryset.exclude(source_pages__transcription__isnull=value)
