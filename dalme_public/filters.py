import copy
from datetime import datetime

from django import forms
from django.db.models import Case, F, Q, When
from django.forms.widgets import NullBooleanSelect

import django_filters

from dalme_app.models import Attribute, Source
from dalme_public.models import Collection, Set


BOOLEAN_CHOICES = [('true', 'Yes'), ('false', 'No')]


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

def collection_choices():
    return [
        (collection.pk, collection.title)
        for collection in Collection.objects.all().order_by('title')
    ]


def dataset_choices():
    return [
        (dataset.pk, dataset.title)
        for dataset in Set.objects.all().order_by('title')
    ]


def source_type_choices():
    type_map = _map_source_types()
    return sorted(list(type_map.items()), key=lambda choice: choice[1])


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
        # eliminated on the endpoint itself before going down the wire.
        date = self.get_value('date', value)
        if date:
            self.parent.annotated = True
            # TODO: It's not perfect, but probably as good as we are going
            # to get without going deep into date data normalization.
            qs = self.annotate_dates(qs)
            if date.startswith('-'):
                qs = qs.order_by(
                    F('start_date').desc(nulls_first=True),
                    F('end_date').desc(nulls_last=True)
                )
            else:
                qs = qs.order_by(
                    F('start_date').asc(nulls_last=True),
                    F('end_date').asc(nulls_last=True),
                )

        source_type = self.get_value('source_type', value)
        if source_type:
            self.parent.annotated = True
            # TODO: This isn't right I don't think!!
            qs = qs.annotate(
                source_type=Case(
                    When(
                        attributes__attribute_type__short_name='record_type',
                        then=F('attributes__value_STR')
                    ),
                    default=None
                )
            ).distinct()
            if source_type.startswith('-'):
                qs = qs.order_by(F('source_type').desc(nulls_first=True))
            else:
                qs = qs.order_by(F('source_type').asc(nulls_last=True))

        return qs


class SourceFilterForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()

        date_range = self.data.get('date_range')
        if date_range:
            try:
                after, before = date_range.split(',')
            except ValueError:
                self.add_error(
                    'date_range', f'Incorrect date format, should be: %Y,%Y'
                )
            after = f'{after}-01-01'
            before = f'{before}-12-31'

            try:
                after, before = [
                    datetime.strptime(value, '%Y-%m-%d')
                    for value in [after, before]
                ]
            except ValueError:
                self.add_error(
                    'date_range',
                    f'Malformed date value for an element of: {date_range}'
                )

            cleaned_data['date_range'] = [after, before]

        return cleaned_data


class SourceFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.annotated = False
        super().__init__(*args, **kwargs)
        for definition in self.filters.values():
            definition.field.label_suffix = ''

    name = django_filters.CharFilter(label='Name', lookup_expr='icontains')
    source_type = django_filters.MultipleChoiceFilter(
        label='Type',
        choices=source_type_choices,
        method='filter_type'
    )
    date_range = django_filters.DateFromToRangeFilter(
        label='Date Range',
        method='filter_date_range'
    )
    collection = django_filters.ChoiceFilter(
        label='Collection',
        choices=collection_choices,
        method='filter_collection'
    )
    dataset = django_filters.ChoiceFilter(
        label='Set',
        choices=dataset_choices,
        method='filter_dataset'
    )
    has_image = django_filters.ChoiceFilter(
        label='Has Image', method='filter_image', choices=BOOLEAN_CHOICES
    )
    has_transcription = django_filters.ChoiceFilter(
        label='Has Transcription', method='filter_transcription', choices=BOOLEAN_CHOICES
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

        after, before = value
        if after:
            queryset = queryset.filter(attributes__value_DATE__gte=after)
        if before:
            queryset = queryset.filter(attributes__value_DATE__lte=before)

        return queryset

    def filter_collection(self, queryset, name, value):
        try:
            collection = Collection.objects.get(pk=value)
        except Collection.DoesNotExist:
            return queryset.none()
        return queryset.filter(
            sets__set_id__in=[
                dataset.specific.source_set.pk
                for dataset in collection.get_children()
            ]
        )

    def filter_dataset(self, queryset, name, value):
        try:
            dataset = Set.objects.get(pk=value)
        except Set.DoesNotExist:
            return queryset.none()
        return queryset.filter(sets__set_id=dataset.source_set.pk)

    def filter_image(self, queryset, name, value):
        value = True if value == 'true' else False
        return queryset.exclude(source_pages__page__dam_id__isnull=value)

    def filter_transcription(self, queryset, name, value):
        value = True if value == 'true' else False
        return queryset.exclude(source_pages__transcription__isnull=value)
