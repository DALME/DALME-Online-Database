import itertools

from django.db.models import OuterRef, Subquery

import django_filters

from dalme_app.models import Attribute, Source
from dalme_public import forms
from dalme_public.models import (
    Collection,
    Corpus,
    Essay,
    FeaturedInventory,
    FeaturedObject,
)


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


def corpus_choices():
    return [
        (corpus.pk, corpus.title)
        for corpus in Corpus.objects.all().order_by('title')
    ]


def collection_choices():
    return [
        (collection.pk, collection.title)
        for collection in Collection.objects.all().order_by('title')
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
    def annotate_dates(qs):
        # These results are not 100% perfect. Some end up incorrectly
        # annotated with None because certain start_date attributes objects do
        # have a value_STR but don't have a value_DATE. This could be fixed
        # with a data migration adding in the missing datetime values to the
        # objects. To see the rows in question, call the following.
        # Attribute.objects.filter(
        #     attribute_type_id=26, value_DATE__isnull=True
        # )
        start_dates = Attribute.objects.filter(
            sources=OuterRef('pk'),
            attribute_type__short_name='start_date'
        )
        return qs.annotate(
            source_date=Subquery(start_dates.values('value_DATE')[:1])
        ).distinct()

    @staticmethod
    def annotate_source_type(qs):
        record_types = Attribute.objects.filter(
            sources=OuterRef('pk'),
            attribute_type__short_name='record_type'
        )
        return qs.annotate(
            source_type=Subquery(record_types.values('value_STR')[:1])
        ).distinct()

    def filter(self, qs, value):
        qs = super().filter(qs, value=list())
        # For now any duplicates that remain here after filtering are
        # eliminated on the endpoint itself before going down the wire.
        # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#distinct
        date = self.get_value('date', value)
        if date:
            self.parent.annotated = True
            qs = self.annotate_dates(qs)

        source_type = self.get_value('source_type', value)
        if source_type:
            self.parent.annotated = True
            qs = self.annotate_source_type(qs)

        return qs


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
    corpus = django_filters.ChoiceFilter(
        label='Corpus',
        choices=corpus_choices,
        method='filter_corpus'
    )
    collection = django_filters.ChoiceFilter(
        label='Collection',
        choices=collection_choices,
        method='filter_collection'
    )
    has_image = django_filters.ChoiceFilter(
        label='Has Image', method='filter_image', choices=BOOLEAN_CHOICES
    )
    has_transcription = django_filters.ChoiceFilter(
        label='Has Transcription',
        method='filter_transcription',
        choices=BOOLEAN_CHOICES
    )

    order_by = SourceOrderingFilter(
        fields=(('name', 'name'),)
    )

    class Meta:
        model = Source
        form = forms.SourceFilterForm
        fields = [
            'name',
            'source_type',
            'date_range',
            'corpus',
            'collection',
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

    def filter_corpus(self, queryset, name, value):
        try:
            corpus = Corpus.objects.get(pk=value)
        except Corpus.DoesNotExist:
            return queryset.none()
        return queryset.filter(
            sets__set_id__in=[
                collection.specific.source_set.pk
                for collection in corpus.collections.all()
            ]
        )

    def filter_collection(self, queryset, name, value):
        try:
            collection = Collection.objects.get(pk=value)
        except Collection.DoesNotExist:
            return queryset.none()
        return queryset.filter(sets__set_id=collection.source_set.pk)

    def filter_image(self, queryset, name, value):
        value = True if value == 'true' else False
        return queryset.exclude(source_pages__page__dam_id__isnull=value)

    def filter_transcription(self, queryset, name, value):
        value = True if value == 'true' else False
        return queryset.exclude(source_pages__transcription__isnull=value)


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
            qs = sorted(qs, key=lambda obj: obj.first_published_at)
            grouped = [
                (key, list(values))
                for key, values in itertools.groupby(
                    qs, key=lambda obj: obj.first_published_at.year
                )
            ]
        else:
            qs = sorted(qs, key=lambda obj: obj.owner.last_name)
            grouped = [
                (key, list(values))
                for key, values in itertools.groupby(
                    qs, key=lambda obj: f'{obj.author}'
                )
            ]
        return grouped


class CollectionsFilter(django_filters.FilterSet):
    pass
