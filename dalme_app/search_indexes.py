from haystack import indexes
from dalme_app.models import *

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
        att_l = Content_type_x_attribute_type.objects.filter(content_type__content_class=1).select_related('attribute_type')
        att_dict = {}
        for a in att_l:
                if a.attribute_type.short_name not in att_dict:
                    att_dict[a.attribute_type.short_name] = [a.attribute_type.name,a.attribute_type.data_type,str(a.attribute_type_id)]
        extra_dict = {}
        for k,v in att_dict.items():
            extra_dict[k] = 'SELECT dalme_app_attribute_'+v[1].lower()+'.value FROM dalme_app_attribute_'+v[1].lower()+' JOIN dalme_app_attribute ON dalme_app_attribute.id = dalme_app_attribute_'+v[1].lower()+'.attribute_id_id JOIN dalme_app_source src2 ON dalme_app_attribute.content_id = src2.id WHERE src2.id = dalme_app_source.id AND dalme_app_attribute.attribute_type = '+v[2]

        extra_dict['transcription'] = 'SELECT transcription FROM dalme_app_transcription WHERE dalme_app_transcription.source_id_id = dalme_app_source.id'

        queryset = Source.objects.all().extra(select=extra_dict)

        return queryset
