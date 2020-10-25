from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from dalme_app.models import Source
from django.core.exceptions import ObjectDoesNotExist


@registry.register_document
class SourceDocument(Document):
    text = fields.TextField()
    type = fields.IntegerField()
    is_public = fields.BooleanField()

    class Index:
        name = 'sources'
        mappings = {
            "properties": {
              "text": {
                "type": "text",
                "index_prefixes": {
                  "min_chars": 2,
                  "max_chars": 10
                }
              }
            }
        }

    class Django:
        model = Source
        fields = ['name']

    def prepare_text(self, instance):
        text = ''
        for attribute in instance.attributes.all():
            text += '{}: {}'.format(attribute.attribute_type.name, str(attribute))

        for page in instance.source_pages.all():
            try:
                text += page.transcription.transcription
            except AttributeError:
                pass
        return text

    def prepare_type(self, instance):
        return instance.type.id

    def prepare_is_public(self, instance):
        try:
            return instance.workflow.is_public
        except ObjectDoesNotExist:
            return False


@registry.register_document
class PublicSourceDocument(Document):
    text = fields.TextField()
    has_image = fields.BooleanField()
    has_transcription = fields.BooleanField()
    date = fields.DateField()
    source_type = fields.TextField()
    set_membership = fields.TextField()

    class Index:
        name = 'public_sources'
        mappings = {
            "properties": {
              "text": {
                "type": "text",
                "index_prefixes": {
                  "min_chars": 2,
                  "max_chars": 10
                }
              }
            }
        }

    class Django:
        model = Source
        fields = ['name']

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
        text = ''
        for attribute in instance.attributes.all():
            text += '{}: {}'.format(attribute.attribute_type.name, str(attribute))

        for page in instance.source_pages.all():
            try:
                text += page.transcription.transcription
            except AttributeError:
                pass
        return text

    def get_queryset(self):
        return Source.objects.filter(type=13, workflow__is_public=True)
