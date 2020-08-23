from haystack import indexes
from dalme_app.models import (Attribute_type, CityReference, CountryReference,
                              LanguageReference, Profile, RightsPolicy, Set, Source, Task, Ticket)
from django.core.exceptions import ObjectDoesNotExist


class Attribute_typeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/attribute_types.txt")

    def get_model(self):
        return Attribute_type

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class CityReferenceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/cities.txt")

    def get_model(self):
        return CityReference

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class CountryReferenceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/countries.txt")

    def get_model(self):
        return CountryReference

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class LanguageReferenceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/languages.txt")

    def get_model(self):
        return LanguageReference

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/profiles.txt")

    def get_model(self):
        return Profile

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class RightsPolicyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/rights_policies.txt")

    def get_model(self):
        return RightsPolicy

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class SetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/sets.txt")

    def get_model(self):
        return Set

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class SourceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True, template_name="search/sources.txt")
    name = indexes.CharField(model_attr='name')
    type = indexes.IntegerField()
    is_public = indexes.BooleanField()

    def get_model(self):
        return Source

    def prepare_type(self, obj):
        return obj.type.id

    def prepare_is_public(self, obj):
        try:
            return obj.workflow.is_public
        except ObjectDoesNotExist:
            return False

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class TaskIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/tasks.txt")

    def get_model(self):
        return Task

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class TicketIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/tickets.txt")

    def get_model(self):
        return Ticket

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
