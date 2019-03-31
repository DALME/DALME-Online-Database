from haystack import indexes
from dalme_app.models import *
from django.db.models.expressions import RawSQL

class Attribute_typeIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/attribute_types.txt")

    def get_model(self):
        return Attribute_type

    def index_queryset(self, using=None):
            return self.get_model().objects.all()

class SourceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/sources.txt")

    def get_model(self):
        return Source

    def index_queryset(self, using=None):
        #NEED TO ADD TEXT FIELD FOR COMMENTS AND ALSO INT + DATE?
        queryset = Source.objects.all().annotate(att_blob=RawSQL('SELECT GROUP_CONCAT(dalme_app_attribute.value_STR SEPARATOR ",") FROM dalme_app_attribute JOIN dalme_app_source src2 ON dalme_app_attribute.object_id = src2.id WHERE src2.id = dalme_app_source.id', []))
        # NEED TO ADD TRANSCRIPTIONS queryset = queryset.select_related('pages__')

        return queryset
