from haystack import indexes
from dalme_app.models import (Source, Attribute_type)
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
        queryset = Source.objects.all().annotate(str_blob=RawSQL('SELECT GROUP_CONCAT(dalme_app_attribute.value_STR SEPARATOR ",") \
                                                                  FROM dalme_app_attribute JOIN dalme_app_source src2 ON dalme_app_attribute.object_id = src2.id \
                                                                  WHERE src2.id = dalme_app_source.id', []))
        queryset = queryset.annotate(txt_blob=RawSQL('SELECT GROUP_CONCAT(dalme_app_attribute.value_TXT SEPARATOR ",") \
                                                      FROM dalme_app_attribute JOIN dalme_app_source src2 ON dalme_app_attribute.object_id = src2.id \
                                                      WHERE src2.id = dalme_app_source.id', []))
        queryset = queryset.annotate(int_blob=RawSQL('SELECT GROUP_CONCAT(dalme_app_attribute.value_INT SEPARATOR ",") \
                                                      FROM dalme_app_attribute JOIN dalme_app_source src2 ON dalme_app_attribute.object_id = src2.id \
                                                      WHERE src2.id = dalme_app_source.id', []))
        queryset = queryset.annotate(transcriptions=RawSQL('SELECT GROUP_CONCAT(dalme_app_transcription.transcription SEPARATOR "|") \
                                                            FROM dalme_app_transcription \
                                                            JOIN dalme_app_source_pages ON dalme_app_transcription.id = dalme_app_source_pages.transcription_id \
                                                            JOIN dalme_app_source src2 ON dalme_app_source_pages.source_id = src2.id \
                                                            WHERE src2.id = dalme_app_source.id', []))
        return queryset
