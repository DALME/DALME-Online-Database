"""API endpoint for returning filter options."""

from django.http import JsonResponse
from django.urls import path
from django.views import View

from public.extensions.records.models import Corpus
from public.filters import locale_choices, map_record_types
from public.models import Collection


class FilterChoices(View):
    """API endpoint for returning filter options."""

    @classmethod
    def get_urlpatterns(cls):
        return [path('', cls.as_view(), name='choices')]

    def corpus_choices(self):
        """Return options for `corpus`."""
        choices = [{'value': corpus.pk, 'text': corpus.title} for corpus in Corpus.objects.all().order_by('title')]
        return [{'value': '', 'text': 'Filter by corpus', 'disabled': True}, *choices]

    def collection_choices(self):
        """Return options for `collection`."""
        choices = [
            {'value': collection.pk, 'text': collection.title}
            for collection in Collection.objects.all().order_by('title')
        ]
        return [{'value': '', 'text': 'Filter by collection', 'disabled': True}, *choices]

    def record_type_choices(self):
        """Return options for `record_type`."""
        types = map_record_types()
        choices = sorted(
            [{'value': str(idx), 'text': value} for idx, value in types.items()],
            key=lambda choice: choice['text'],
        )
        return [{'value': '', 'text': 'Filter by record type', 'disabled': True}, *choices]

    def locale_choices_as_dict(self):
        """Return options for `locale`."""
        choices = [{'value': i[0], 'text': i[1]} for i in locale_choices()]
        return [{'value': '', 'text': 'Filter by locale', 'disabled': True}, *choices]

    @property
    def methods(self):
        """Redirect request to the appropriate method."""
        return {
            'corpusChoices': self.corpus_choices,
            'collectionChoices': self.collection_choices,
            'recordTypeChoices': self.record_type_choices,
            'localeChoices': self.locale_choices_as_dict,
        }

    def get_data(self):
        """Return the options data."""
        return {key: func() for key, func in self.methods.items()}

    def get(self, request):  # noqa: ARG002
        """Return the requested data."""
        return JsonResponse(self.get_data())
