"""Define Elasticsearch documents."""

from contextlib import suppress

from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Index, Mapping, normalizer
from elasticsearch_dsl import Join as dsl_Join

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from ida.models import PageNode, Record


class JoinField(fields.DEDField, dsl_Join):
    """Join field class."""

    def __init__(self, *args, **kwargs):
        public = kwargs.pop('public', False)
        self._public = public
        kwargs['relations'] = {'PublicRecord': 'PublicFolio'} if public else {'FullRecord': 'FullFolio'}
        super().__init__(*args, **kwargs)

    def get_value_from_instance(self, instance):
        """Return value depending on instance type."""
        if not instance:
            return None

        if isinstance(instance, Record):
            return 'PublicRecord' if self._public else 'FullRecord'

        if isinstance(instance, PageNode):
            return {
                'name': 'PublicFolio' if self._public else 'FullFolio',
                'parent': str(instance.record.id),
            }

        return None


basic_normalizer = normalizer(
    'basic_normalizer',
    type='custom',
    char_filter=[],
    filter=['lowercase', 'asciifolding'],
)

dynamic_template = {
    'standard_string_fields': {
        'match_mapping_type': 'string',
        'mapping': {
            'type': 'keyword',
            'normaliser': basic_normalizer,
        },
    },
}

analysis = {'normalizer': basic_normalizer}
default_mapping = Mapping()
default_mapping.meta('dynamic_templates', **dynamic_template)
public_records = Index('public_records')
public_records.mapping(default_mapping)
public_records.settings(analysis=analysis)
full_records = public_records.clone('full_records')


@public_records.document
class PublicRecordBase(Document):
    """Base public record document."""

    join_field = JoinField(public=True)


@full_records.document
class FullRecordBase(Document):
    """Base record document."""

    join_field = JoinField()


@registry.register_document
class PublicRecord(PublicRecordBase):
    """Published record document."""

    id = fields.KeywordField(attr='id')
    name = fields.TextField(
        attr='name',
        fields={'keyword': fields.KeywordField(normalizer=basic_normalizer)},
        index_prefixes={},
    )
    is_private = fields.BooleanField(attr='is_private')
    is_public = fields.BooleanField()
    parent = fields.TextField(
        attr='parent.name',
        fields={'keyword': fields.KeywordField(normalizer=basic_normalizer)},
        index_prefixes={},
    )
    attributes = fields.ObjectField()
    collections = fields.ObjectField()
    geo_location = fields.GeoPointField()

    class Index:
        name = 'public_records'

    class Django:
        model = Record

    def update(self, thing, refresh=None, action='index', parallel=False, **kwargs):
        """Update index."""
        if isinstance(thing, models.Model) and not thing.is_published and action == 'index':
            action = 'delete'
            kwargs = {**kwargs, 'raise_on_error': False}
        return super().update(thing, refresh, action, parallel, **kwargs)

    def get_queryset(self):
        """Return record queryset."""
        return Record.objects.filter(workflow__is_public=True)

    def prepare_is_public(self, instance):
        """Return boolean indicating published status."""
        return instance.is_published

    def prepare_attributes(self, instance):
        """Prepare document attributes for indexing."""
        attributes = instance.attributes.all()
        if attributes:
            return {a.label: str(a.value) for a in instance.attributes.all()}
        return None

    def prepare_collections(self, instance):
        """Prepare collection for indexing."""
        cols = instance.collections.filter(is_published=True)
        if cols.exists():
            return [{'name': i.set_id.name} for i in cols]
        return [{'name': 'none'}]

    def prepare_credits(self, instance):
        """Prepare document credits for indexing."""
        return instance.get_credits()

    def prepare_geo_location(self, instance):
        """Prepare document location info for indexing."""
        locales = instance.attributes.filter(attribute_type=36)
        if locales.exists():
            locale = locales.first()
            return f'{locale.value.latitude},{locale.value.longitude}'
        return None


@registry.register_document
class PublicFolio(PublicRecordBase):
    """Published folio document."""

    folio = fields.KeywordField(attr='page.name')
    transcription = fields.TextField(
        fields={'keyword': fields.KeywordField(normalizer=basic_normalizer)},
        index_prefixes={},
    )

    class Index:
        name = 'public_records'

    class Django:
        model = PageNode

    def get_queryset(self):
        """Return folio queryset."""
        return PageNode.objects.filter(record__workflow__is_public=True)

    def _prepare_action(self, object_instance, action):
        return {
            '_op_type': action,
            '_index': self._index._name,  # noqa: SLF001
            '_id': self.generate_id(object_instance),
            '_routing': str(object_instance.record.id),
            '_record': (self.prepare(object_instance) if action != 'delete' else None),
        }

    def prepare_transcription(self, instance):
        """Prepare folio transcription for indexing."""
        with suppress(ObjectDoesNotExist):
            return instance.transcription.text_blob


@registry.register_document
class FullRecord(FullRecordBase, PublicRecord):
    """Record document."""

    class Index:
        name = 'full_records'

    def get_queryset(self):
        """Return record queryset."""
        return Record.objects.all()


@registry.register_document
class FullFolio(FullRecordBase, PublicFolio):
    """Folio document."""

    class Index:
        name = 'full_records'

    def get_queryset(self):
        """Return folio queryset."""
        return PageNode.objects.all()
