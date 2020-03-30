from django.db.models import Case, F, Q, When
from django.forms.widgets import NullBooleanSelect

import django_filters

from dalme_app.models import Attribute, Source
from dalme_public.models import Collection, Set


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

def _source_type_choices():
    type_map = _map_source_types()
    return sorted(list(type_map.items()), key=lambda choice: choice[1])


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


class SourceOrderingFilter(django_filters.OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['choices'] += [
            ('source_type', 'Type'),
            ('-source_type', 'Type (descending)'),
            # ('date', 'Date'),
            # ('-date', 'Date (descending)'),
        ]

    @staticmethod
    def get_value(field, value):
        if not value:
            return False
        return next((v for v in value if v and v.endswith(field)), False)

    def filter(self, qs, value):
        qs = super().filter(qs, value)

        date = self.get_value('date', value)
        if date:
            self.parent.annotated = True
            raise NotImplementedError()

        source_type = self.get_value('source_type', value)
        if source_type:
            self.parent.annotated = True
            # TODO: Still looking for a solution to the 'distinct' issue.
            # https://docs.djangoproject.com/en/1.11/ref/models/querysets/#distinct
            # Perhaps, as long as we filter for source_type last, we can cast
            # the results to `values` and the distinct comparison will succeed.
            # In any case, for now any duplicates that remain here are
            # eliminated on the view itself before template render time.
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
        fields = ['name']

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

    def filter_collection(self, queryset, name, value):
        try:
            collection = Collection.objects.get(pk=value)
        except Collection.DoesNotExist:
            return queryset.none()
        source_sets = [dataset.source_set for dataset in collection.sets.all()]
        return queryset.filter(sets__in=source_sets)

    def filter_dataset(self, queryset, name, value):
        try:
            dataset = Set.objects.get(pk=value)
        except Set.DoesNotExist:
            return queryset.none()
        return queryset.filter(sets__in=[dataset.source_set])

    def filter_image(self, queryset, name, value):
        return queryset.exclude(source_pages__page__dam_id__isnull=value)

    def filter_transcription(self, queryset, name, value):
        return queryset.exclude(source_pages__transcription__isnull=value)
