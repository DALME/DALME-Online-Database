from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Join as dsl_Join
from elasticsearch_dsl import Index, Mapping, normalizer
from dalme_app.models import Source, Source_pages, LocaleReference
from django.core.exceptions import ObjectDoesNotExist
import lxml.etree as et
from datetime import date


class JoinField(fields.DEDField, dsl_Join):
    def __init__(self, multi=False, required=False, *args, **kwargs):
        public = kwargs.pop('public', False)
        self._public = public
        kwargs['relations'] = {'PublicSource': 'PublicFolio'} if public else {'FullSource': 'FullFolio'}
        super().__init__(*args, **kwargs)

    def get_value_from_instance(self, instance, field_value_to_ignore=None):
        if not instance:
            return None

        if isinstance(instance, Source):
            return 'PublicSource' if self._public else 'FullSource'

        if isinstance(instance, Source_pages):
            return {
                'name': 'PublicFolio' if self._public else 'FullFolio',
                'parent': str(instance.source.id)
            }


basic_normalizer = normalizer(
    'basic_normalizer',
    type='custom',
    char_filter=[],
    filter=['lowercase', 'asciifolding']
)

dynamic_template = {
    'standard_string_fields': {
        'match_mapping_type': 'string',
        'mapping': {
            'type': 'keyword',
            'normaliser': basic_normalizer
        }
    }
}

analysis = {'normalizer': basic_normalizer}

default_mapping = Mapping()
default_mapping.meta('dynamic_templates', **dynamic_template)

public_sources = Index('public_sources')
public_sources.mapping(default_mapping)
public_sources.settings(analysis=analysis)
full_sources = public_sources.clone('full_sources')


@public_sources.document
class PublicSourceBase(Document):
    join_field = JoinField(public=True)


@full_sources.document
class FullSourceBase(Document):
    join_field = JoinField()


@registry.register_document
class PublicSource(PublicSourceBase):
    id = fields.KeywordField(attr='id')
    name = fields.TextField(
        attr='name',
        fields={'keyword': fields.KeywordField(
            normalizer=basic_normalizer
        )}
    )
    type = fields.IntegerField(attr='type.id')
    is_private = fields.BooleanField(attr='is_private')
    is_public = fields.BooleanField()
    parent = fields.TextField(
        attr='parent.name',
        fields={'keyword': fields.KeywordField(
            normalizer=basic_normalizer
        )}
    )
    attributes = fields.ObjectField()
    collections = fields.ObjectField()
    credits = fields.ObjectField()
    geo_location = fields.GeoPointField()

    class Index:
        name = 'public_sources'

    class Django:
        model = Source

    def get_queryset(self):
        return Source.objects.filter(type=13, workflow__is_public=True)

    def prepare_is_public(self, instance):
        try:
            return instance.workflow.is_public
        except ObjectDoesNotExist:
            return False

    def prepare_attributes(self, instance):
        attribute_list = []
        dates_list = []
        for attribute in instance.attributes.all():
            label = attribute.attribute_type.short_name
            if attribute.attribute_type.data_type == 'DATE':
                if attribute.value_DATE:
                    dates_list.append(attribute.value_DATE.strftime('%Y-%m-%d'))
                elif attribute.value_DATE_y:
                    d = attribute.value_DATE_d or 1
                    m = attribute.value_DATE_m or 1
                    y = attribute.value_DATE_y
                    dates_list.append(date(y, m, d).strftime('%Y-%m-%d'))

            elif attribute.attribute_type.data_type == 'TXT':
                attribute_list.append((label, attribute.value_TXT))

            else:
                attribute_list.append((label, str(attribute)))

        if dates_list:
            attribute_list.append(('date', dates_list))

        if attribute_list:
            return dict(attribute_list)

    def prepare_collections(self, instance):
        try:
            if instance.sets.all().count() > 0:
                cols = [('name', set.set_id.name) for set in instance.sets.all() if set.set_id.set_type == 2]
                if cols:
                    return dict(cols)
                else:
                    return [{'name': 'none'}]
        except ObjectDoesNotExist:
            return [{'name': 'none'}]

    def prepare_credits(self, instance):
        credit_list = []
        for credit in instance.credits.all():
            agent = credit.agent.standard_name
            type = credit.get_type_display()
            credit_list.append({
                'agent': f'{agent} ({type})',
                'type': type
            })
        return credit_list

    def prepare_geo_location(self, instance):
        locales = instance.attributes.filter(attribute_type=36)
        if locales.exists():
            loc_id = locales[0].value_JSON['id']
            locale = LocaleReference.objects.get(id=loc_id)
            return f'{locale.latitude},{locale.longitude}'


@registry.register_document
class PublicFolio(PublicSourceBase):
    folio = fields.KeywordField(attr='page.name')
    transcription = fields.TextField(
        fields={'keyword': fields.KeywordField(
            normalizer=basic_normalizer
        )}
    )

    class Index:
        name = 'public_sources'

    class Django:
        model = Source_pages

    def get_queryset(self):
        return Source_pages.objects.filter(source__type=13, source__workflow__is_public=True)

    def _prepare_action(self, object_instance, action):
        return {
            '_op_type': action,
            '_index': self._index._name,
            '_id': self.generate_id(object_instance),
            '_routing': str(object_instance.source.id),
            '_source': (
                self.prepare(object_instance) if action != 'delete' else None
            ),
        }

    def prepare_transcription(self, instance):
        xml_parser = et.XMLParser(recover=True)
        try:
            try:
                tree = et.fromstring('<xml>' + instance.transcription.transcription + '</xml>', xml_parser)
                return et.tostring(tree, encoding='unicode', xml_declaration=False, method='text')

            except AttributeError:
                pass
        except ObjectDoesNotExist:
            pass


@registry.register_document
class FullSource(FullSourceBase, PublicSource):

    class Index:
        name = 'full_sources'

    def get_queryset(self):
        return Source.objects.all()


@registry.register_document
class FullFolio(FullSourceBase, PublicFolio):

    class Index:
        name = 'full_sources'

    def get_queryset(self):
        return Source_pages.objects.all()
