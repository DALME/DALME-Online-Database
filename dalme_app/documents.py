from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from dalme_app.models import Source
from django.core.exceptions import ObjectDoesNotExist
import lxml.etree as et


@registry.register_document
class SourceDocument(Document):
    name = fields.TextField()
    text = fields.TextField()
    has_image = fields.BooleanField()
    has_transcription = fields.BooleanField()
    date = fields.DateField()
    source_type = fields.KeywordField()
    set_membership = fields.TextField()
    is_public = fields.BooleanField()
    type = fields.IntegerField()

    class Index:
        name = 'sources'

    class Django:
        model = Source

    def prepare_name(self, instance):
        return instance.name

    def prepare_type(self, instance):
        return instance.type.id

    def prepare_is_public(self, instance):
        try:
            return instance.workflow.is_public
        except ObjectDoesNotExist:
            return False

    def prepare_has_image(self, instance):
        return instance.has_images

    def prepare_has_transcription(self, instance):
        return instance.has_transcriptions

    def prepare_date(self, instance):
        if instance.attributes.filter(attribute_type__short_name='start_date').exists():
            return instance.attributes.filter(attribute_type__short_name='start_date').first().value_DATE
        elif instance.attributes.filter(attribute_type__short_name='end_date').exists():
            return instance.attributes.filter(attribute_type__short_name='end_date').first().value_DATE
        else:
            return None

    def prepare_source_type(self, instance):
        if instance.attributes.filter(attribute_type__short_name='record_type').exists():
            return instance.attributes.filter(attribute_type__short_name='record_type').first().value_STR
        else:
            return None

    def prepare_set_membership(self, instance):
        return ','.join([str(set['set_id_id']) for set in instance.sets.all().values()])

    def prepare_text(self, instance):
        text = instance.name + '\n'
        xml_parser = et.XMLParser(recover=True)
        for attribute in instance.attributes.all():
            text += '{}: {}\n'.format(attribute.attribute_type.name, str(attribute))

        for page in instance.source_pages.all():
            try:
                tree = et.fromstring('<xml>' + page.transcription.transcription + '</xml>', xml_parser)
                text += et.tostring(tree, encoding='unicode', xml_declaration=False, method='text')
            except AttributeError:
                pass
        return text


@registry.register_document
class PublicSourceDocument(SourceDocument):

    class Index:
        name = 'public_sources'

    def get_queryset(self):
        return Source.objects.filter(type=13, workflow__is_public=True)
