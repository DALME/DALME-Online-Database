"""Define filters for dalme_public."""
import calendar
import itertools

import django_filters

from django.db.models import OuterRef, Q, Subquery

from dalme_public import forms
from dalme_public.models import (
    Collection,
    Corpus,
    Essay,
    FeaturedInventory,
    FeaturedObject,
)
from ida.models import Attribute, LocaleReference, Record

BOOLEAN_CHOICES = [('true', 'Yes'), ('false', 'No')]


def _map_record_types():
    # We have to filter over 'value_str' rather than, say, 'pk' because of the
    # sideways denormalization scheme: there is no unique, one-to-one mapping
    # between Attributes with the same 'value_str'. Compare:
    #
    #     attrs = Attribute.objects.filter(
    #         attribute_type__short_name='record_type'
    #     )
    #     set([x.value_str for x in attrs])
    #     set([(x.pk, x.value_str) for x in attrs])
    #
    # So, let's eliminate the duplicates and index the choices first before
    # sorting them for the frontend widget, that way we can reaccess them by
    # index later to get the right names back when a request with a query comes
    # in. See the `filter_type` method below.

    return {
        str(idx): attr['attributevaluestr__value']
        for idx, attr in enumerate(
            Attribute.objects.filter(
                attribute_type__name='record_type',
                object_id__in=Record.objects.filter(workflow__is_public=True).values('id'),
            )
            .values('attributevaluestr__value')
            .distinct(),
        )
    }


def corpus_choices():
    return [(corpus.pk, corpus.title) for corpus in Corpus.objects.all().order_by('title')]


def collection_choices():
    return [(collection.pk, collection.title) for collection in Collection.objects.all().order_by('title')]


def record_type_choices():
    type_map = _map_record_types()
    return sorted(type_map.items(), key=lambda choice: choice[1])


def locale_choices():
    locales = [
        int(i)
        for i in Attribute.objects.filter(
            attribute_type=36,
            record__workflow__is_public=True,
        )
        .values_list(
            'attributevaluefkey__locale__id',
            flat=True,
        )
        .distinct()
    ]

    return [(i.id, i.name) for i in LocaleReference.objects.filter(id__in=locales).order_by('name')]


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

    def filter(self, qs, value):  # noqa: A003
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


class RecordFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        self.annotated = False
        super().__init__(*args, **kwargs)
        for definition in self.filters.values():
            definition.field.label_suffix = ''

    name = django_filters.CharFilter(
        label='Name',
        lookup_expr='icontains',
    )
    record_type = django_filters.MultipleChoiceFilter(
        label='Type',
        choices=record_type_choices,
        method='filter_type',
    )
    date_range = django_filters.DateFromToRangeFilter(
        label='Date Range',
        method='filter_date_range',
    )
    corpus = django_filters.ChoiceFilter(
        label='Corpus',
        choices=corpus_choices,
        method='filter_corpus',
    )
    collection = django_filters.ChoiceFilter(
        label='Collection',
        choices=collection_choices,
        method='filter_collection',
    )
    has_image = django_filters.ChoiceFilter(
        label='Has Image',
        method='filter_image',
        choices=BOOLEAN_CHOICES,
    )
    has_transcription = django_filters.ChoiceFilter(
        label='Has Transcription',
        method='filter_transcription',
        choices=BOOLEAN_CHOICES,
    )
    locale = django_filters.ChoiceFilter(
        label='Locale',
        choices=locale_choices,
        method='filter_locale',
    )

    order_by = RecordOrderingFilter()

    class Meta:
        model = Record
        form = forms.RecordFilterForm
        fields = [
            'name',
            'record_type',
            'date_range',
            'corpus',
            'collection',
            'has_transcription',
            'has_image',
            'locale',
            'order_by',
        ]

    def filter_type(self, queryset, name, value):  # noqa: ARG002
        # Now we can re-use the type map when a request comes in for filtering.
        type_map = _map_record_types()
        record_types = []
        for idx in value:
            try:
                record_types.append(type_map[idx])
            except KeyError:
                continue
        return queryset.filter(
            attributes__attributevaluestr__value__in=record_types,
        )

    def filter_date_range(self, queryset, name, value):  # noqa: ARG002
        queryset = queryset.filter(
            attributes__attribute_type__id__in=[19, 25, 26],
        ).distinct()

        after, before = value
        if after:
            queryset = queryset.filter(attributes__attributevaluedate__year__gte=after)
        if before:
            queryset = queryset.filter(attributes__attributevaluedate__year__lte=before)

        return queryset

    def filter_corpus(self, queryset, name, value):  # noqa: ARG002
        try:
            corpus = Corpus.objects.get(pk=value)
        except Corpus.DoesNotExist:
            return queryset.none()
        return queryset.filter(
            collections__collection_id__in=[
                collection.specific.source_set.pk for collection in corpus.collections.all()
            ],
        )

    def filter_collection(self, queryset, name, value):  # noqa: ARG002
        try:
            collection = Collection.objects.get(pk=value)
        except Collection.DoesNotExist:
            return queryset.none()
        return queryset.filter(collections__collection_id=collection.source_set.pk)

    def filter_image(self, queryset, name, value):  # noqa: ARG002
        value = value == 'true'
        return queryset.exclude(folios__page__dam_id__isnull=value)

    def filter_transcription(self, queryset, name, value):  # noqa: ARG002
        value = value == 'true'
        return queryset.exclude(folios__transcription__isnull=value)

    def filter_locale(self, queryset, name, value):  # noqa: ARG002
        return queryset.filter(attributes__attribute_type=36, attributes__attributevaluefkey__locale__id=str(value))


class FeaturedFilter(django_filters.FilterSet):
    @property
    def qs(self):
        qs = super().qs

        kind = self.data.get('kind')
        if kind:
            model = {
                'essay': Essay,
                'inventory': FeaturedInventory,
                'object': FeaturedObject,
            }.get(kind)
            if model:
                qs = [page for page in qs if isinstance(page, model)]

        order = self.data.get('order_by', 'date')
        if order == 'date':
            grouped = []
            qs = sorted(qs, key=lambda obj: obj.last_published_at, reverse=True)
            by_year = [
                (key, list(values))
                for key, values in itertools.groupby(
                    qs,
                    key=lambda obj: obj.last_published_at.year,
                )
            ]
            for year, values in by_year:
                by_month = [
                    (key, list(values))
                    for key, values in itertools.groupby(
                        values,
                        key=lambda obj: calendar.month_name[obj.last_published_at.month],
                    )
                ]
                grouped.append((year, by_month))
        else:
            qs = sorted(qs, key=lambda obj: obj.owner.last_name)
            grouped = [
                (key, list(values))
                for key, values in itertools.groupby(
                    qs,
                    key=lambda obj: f'{obj.author}',
                )
            ]

        return grouped
