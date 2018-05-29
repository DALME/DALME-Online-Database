import datetime
from haystack import indexes
from .models import Agents, Attribute_types, Attributes, Attributes_DATE, Attributes_DBR, Attributes_INT, Attributes_STR, Attributes_TXT, Concepts, Content_classes, Content_types, Content_types_x_attribute_types, Headwords, Objects, Object_attributes, Places, Sources, Pages, Transcriptions, Identity_phrases, Object_phrases, Word_forms, Tokens, Identity_phrases_x_entities


class SourceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Sources
