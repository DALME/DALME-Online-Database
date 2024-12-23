"""Migrate the attribute types."""

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction

from domain.models import (
    AttributeType,
    ContentAttributes,
    ContentTypeExtended,
)

from .base import BaseStage

CT_DATA = {
    'agent': {
        'name': 'Agent',
        'app_label': 'domain',
        'description': 'The direct performer or driver of an action (e.g. a person, an organization).',
        'atypes': [
            'id',
            'name',
            'type',
            'comments',
            'tags',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'organization': {
        'name': 'Organization',
        'app_label': 'domain',
        'description': 'An organization such as a school, NGO, corporation, club, etc.',
        'parent': 'agent',
        'atypes': [
            'short_name',
            'url',
        ],
    },
    'person': {
        'name': 'Person',
        'app_label': 'domain',
        'description': 'A person (alive, dead, undead, or fictional).',
        'parent': 'agent',
        'atypes': ['social_status', 'religion', 'sex', 'legal_persona'],
    },
    'group': {
        'name': 'User Group',
        'app_label': 'auth',
        'description': 'A group of user accounts in the system.',
        'atypes': [],
    },
    'user': {
        'name': 'User Account',
        'app_label': 'oauth',
        'description': "A person's account in the system.",
        'atypes': [
            'last_name',
            'first_name',
            'password',
            'last_login',
            'is_superuser',
            'username',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'full_name',
            'groups',
        ],
    },
    'place': {
        'name': 'Place',
        'app_label': 'domain',
        'description': 'A physical or abstract location.',
        'atypes': [
            'id',
            'name',
            'comments',
            'tags',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'location': {
        'name': 'Location',
        'app_label': 'domain',
        'description': 'A fixed, physical location.',
        'atypes': [
            'id',
            'type',
            'comments',
            'tags',
            'street_address',
            'postal_code',
            'pobox_number',
            'latitude',
            'longitude',
            'elevation',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'countryreference': {
        'name': 'Country',
        'app_label': 'domain',
        'description': 'A country.',
        'parent': 'location',
        'atypes': [
            'id',
            'name',
            'alpha_3_code',
            'alpha_2_code',
            'num_code',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'localereference': {
        'name': 'Locale',
        'app_label': 'domain',
        'description': 'A geographic place at which there is or was human activity',
        'parent': 'location',
        'atypes': [
            'id',
            'name',
            'administrative_region',
            'country',
            'latitude',
            'longitude',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'languagereference': {
        'name': 'Language',
        'app_label': 'domain',
        'description': 'A structured system of communication that consists of grammar and vocabulary.',
        'atypes': [
            'id',
            'glottocode',
            'iso6393',
            'type',
            'parent',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'collection': {
        'name': 'Collection',
        'app_label': 'domain',
        'description': 'A collection of items.',
        'atypes': [
            'id',
            'name',
            'description',
            'is_public',
            'is_corpus',
            'owner',
            'permissions',
            'comments',
            'member_count',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'rightspolicy': {
        'name': 'Rights Policy',
        'app_label': 'domain',
        'description': 'Guidelines and restrictions regulating the use of a resource.',
        'atypes': [
            'id',
            'name',
            'rights_status',
            'rights_notice',
            'licence',
            'rights',
            'rights_holder',
            'notice_display',
            'default_rights',
            'attachments',
            'comments',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'recordgroup': {
        'name': 'Record Group',
        'app_label': 'domain',
        'description': 'An organized unit (folder, volume, etc.) of documents grouped together either for current use or in the process of archival arrangement.',
        'atypes': [
            'id',
            'name',
            'short_name',
            'description',
            'parent',
            'type',
            'owner',
            'permissions',
            'comments',
            'tags',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
            'mk2_identifier',
            'mk1_identifier',
            'alt_identifier',
            'authority',
            'format',
            'support',
        ],
    },
    'publication': {
        'name': 'Publication',
        'app_label': 'domain',
        'description': 'A written work of fiction or nonfiction.',
        'atypes': [
            'id',
            'name',
            'short_name',
            'description',
            'type',
            'zotero_key',
            'permissions',
            'comments',
            'tags',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
            'mk2_identifier',
            'mk1_identifier',
            'alt_identifier',
        ],
    },
    'record': {
        'name': 'Record',
        'app_label': 'domain',
        'description': 'The smallest intellectually indivisible archival unit (e.g. a letter, memorandum, report, leaflet, or photograph). For example, a book or record album would be described as an item, but the individual chapters of the book or the discs or songs that make up the album would not be described as items.',
        'atypes': [
            'id',
            'name',
            'short_name',
            'description',
            'parent',
            'owner',
            'permissions',
            'comments',
            'tags',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
            'mk2_identifier',
            'mk1_identifier',
            'alt_identifier',
            'archival_series',
            'archival_number',
            'date',
            'end_date',
            'start_date',
            'record_type',
            'record_type_phrase',
            'debt_phrase',
            'debt_amount',
            'debt_unit',
            'debt_unit_type',
            'debt_source',
            'has_inventory',
            'locale',
            'named_persons',
            'has_image',
            'collections',
            'no_folios',
            'has_pages',
            'is_public',
            'language',
        ],
    },
}

CTA_PROPS = {
    ('record', 'language'): {'is_unique': False},
}

RENAMES = {
    'creation_username': 'creation_user',
    'modification_username': 'modification_user',
    'is_public': 'is_published',
}

TO_FKEY = [
    'owner',
    'parent',
    'creation_username',
    'modification_username',
    'type',
    'same_as',
    'record_type',
]

TO_BOOL = [
    'has_inventory',
    'is_superuser',
    'is_staff',
    'is_active',
    'has_image',
    'has_pages',
    'help_flag',
    'notice_display',
    'is_public',
]

TO_INT = ['rights_status']

TO_RREL = [
    'comments',
    'named_persons',
    'collections',
    'permissions',
    'groups',
    'tags',
    'attachments',
]

TO_LOCAL = [
    'id',
    'creation_username',
    'modification_username',
    'creation_timestamp',
    'modification_timestamp',
    'owner',
    'name',
    'short_name',
    'password',
    'last_login',
    'is_superuser',
    'username',
    'email',
    'is_staff',
    'is_active',
    'date_joined',
    'full_name',
    'file_size',
    'required',
    'glottocode',
    'iso6393',
    'alpha_3_code',
    'alpha_2_code',
    'num_code',
    'administrative_region',
    'file',
    'last_modified',
    'last_user',
    'rights_status',
    'rights_notice',
    'licence',
    'rights',
    'rights_holder',
    'notice_display',
    'default_rights',
    'last_name',
    'first_name',
    'has_image',
    'no_folios',
    'same_as',
    'has_pages',
    'help_flag',
    'member_count',
]

NEW_TYPES = [
    {
        'name': 'collection_metadata',
        'label': 'Collection metadata',
        'description': 'A series of key-value pairs defining metadata values associated with a collection.',
        'data_type': 'JSON',
        'is_local': False,
        'source': 'DALME',
    },
    {
        'name': 'workset_progress',
        'label': 'Workset Progress Tracking',
        'description': 'Data attribute for tracking progress in a workset-type collection.',
        'data_type': 'JSON',
        'source': 'DALME',
        'is_local': False,
    },
    {
        'name': 'corpus',
        'label': 'Corpus',
        'description': 'A cohesive collection of texts or documents collated according to subject-specific criteria.',
        'data_type': 'FKEY',
        'source': 'DALME',
        'is_local': False,
    },
    {
        'name': 'collection',
        'label': 'Collection',
        'description': 'A group of resources.',
        'data_type': 'FKEY',
        'source': 'DALME',
        'is_local': False,
    },
]


class Stage(BaseStage):
    """Data migration for attributes types."""

    name = '05 Attribute Types'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.update_attribute_types_sequence()
        self.migrate_attribute_types()
        self.create_new_attribute_types()
        self.migrate_contenttype_extended()

    @transaction.atomic
    def update_attribute_types_sequence(self):
        """Update AttributeType sequence start to account for manually inserted rows."""
        if AttributeType.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Updating AttributeType sequence start')
                cursor.execute(
                    'ALTER TABLE IF EXISTS public.domain_attributetype\
                        ALTER COLUMN id RESTART SET START 154;',
                )

    @transaction.atomic
    def migrate_attribute_types(self):
        """Copy object attribute type data."""
        if AttributeType.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating attribute types')
                cursor.execute('SELECT * FROM restore.core_attribute_type;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    row.pop('options_list')
                    short_name = row.pop('short_name')

                    row.update(
                        {
                            'label': row.pop('name'),
                            'name': RENAMES.get(short_name, short_name),
                            'is_local': short_name in TO_LOCAL,
                            'same_as_id': row.pop('same_as'),
                        },
                    )

                    if short_name in TO_FKEY:
                        row['data_type'] = 'FKEY'
                    elif short_name in TO_BOOL:
                        row['data_type'] = 'BOOL'
                    elif short_name in TO_INT:
                        row['data_type'] = 'INT'
                    elif short_name in TO_RREL:
                        row['data_type'] = 'RREL'
                    elif row['data_type'] == 'TXT':
                        row['data_type'] = 'STR'
                    elif row['data_type'] == 'DEC':
                        row['data_type'] = 'FLOAT'
                    elif row['data_type'] in ['FK-UUID', 'FK-INT']:
                        row['data_type'] = 'FKEY'

                    objs.append(AttributeType(**row))

                AttributeType.objects.bulk_create(objs)
                self.logger.info('Created %s AttributeType instances', AttributeType.objects.count())
        else:
            self.logger.warning('AttributeType data already exists')

    @transaction.atomic
    def create_new_attribute_types(self):
        """Create new attribute types."""
        User = get_user_model()  # noqa: N806
        user_obj = User.objects.get(pk=1)

        self.logger.info('Creating new attribute types...')
        for new_type in NEW_TYPES:
            if AttributeType.objects.filter(name=new_type['name']).exists():
                self.logger.warning('Attribute type "%s" already exists.', new_type['name'])
            else:
                AttributeType.objects.create(
                    **new_type,
                    creation_user=user_obj,
                    modification_user=user_obj,
                )

    @transaction.atomic
    def migrate_contenttype_extended(self):
        """Copy extended content type data.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0011_data_m_contenttypes.py#L274

        """
        if ContentTypeExtended.objects.count() == 0:
            self.logger.info('Migrating extended content types')

            for model, payload in CT_DATA.items():
                app_label = payload['app_label']

                # This should just work as there aren't any renamed or
                # relocated models in the fixtures or anything else tricky.
                ctype = ContentType.objects.get(app_label=app_label, model=model)

                if parent := payload.get('parent'):
                    # The fixtures are arranged in dependency order so we can
                    # assume this already exists if it's specified (ie. we just
                    # made it earlier in the loop).
                    parent = ContentTypeExtended.objects.get(model=parent)

                new_cte = ContentTypeExtended.objects.create(
                    contenttype_ptr=ctype,
                    app_label=app_label,
                    model=model,
                    name=payload['name'],
                    parent=parent,
                    description=payload['description'],
                    is_abstract=False,
                )

                if atypes := payload.get('atypes'):
                    for at_name in atypes:
                        q = AttributeType.objects.filter(name=at_name)
                        if q.exists():
                            atype = q.first()
                            props = {'content_type': new_cte, 'attribute_type': atype}
                            if (new_cte.model, atype.name) in CTA_PROPS:
                                props.update(CTA_PROPS[(new_cte.model, atype.name)])
                            ContentAttributes.objects.create(**props)

            self.logger.info('Created %s ContentTypeExtended instances', ContentTypeExtended.objects.count())
        else:
            self.logger.warning('ContentTypeExtended data already exists')
