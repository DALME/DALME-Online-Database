"""Filter for records."""

import django_filters

from ida.models import Attribute, LocaleReference, Record
from public import forms
from public.extensions.records.models import Corpus
from public.filters.record_ordering import RecordOrderingFilter
from public.models import Collection

BOOLEAN_CHOICES = [('true', 'Yes'), ('false', 'No')]


def map_record_types():
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
    type_map = map_record_types()
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
        type_map = map_record_types()
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
