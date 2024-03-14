"""Migrate the attribute types."""

from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction

from ida.models import (
    AttributeType,
    ContentAttributes,
    ContentTypeExtended,
    OptionsList,
    Tenant,
)

from .base import BaseStage

CT_DATA = {
    'agent': {
        'name': 'Agent',
        'app_label': 'ida',
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
        'app_label': 'ida',
        'description': 'An organization such as a school, NGO, corporation, club, etc.',
        'parent': 'agent',
        'atypes': [
            'short_name',
            'url',
        ],
    },
    'person': {
        'name': 'Person',
        'app_label': 'ida',
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
        'app_label': 'ida',
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
        'app_label': 'ida',
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
        'app_label': 'ida',
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
        'app_label': 'ida',
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
        'app_label': 'ida',
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
        'app_label': 'ida',
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
        'app_label': 'ida',
        'description': 'A collection of items.',
        'atypes': [
            'id',
            'name',
            'description',
            'is_public',
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
        'app_label': 'ida',
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
        'app_label': 'ida',
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
        'app_label': 'ida',
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
        'app_label': 'ida',
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
        ],
    },
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


class Stage(BaseStage):
    """Data migration for attributes types."""

    name = '05 Attribute Types'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.update_attribute_types_sequence()
        self.migrate_attribute_types()
        self.migrate_contenttype_extended()
        self.migrate_options_list()

    @transaction.atomic
    def update_attribute_types_sequence(self):
        """Update AttributeType sequence start to account for manually inserted rows."""
        if AttributeType.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Updating AttributeType sequence start')
                cursor.execute(
                    'ALTER TABLE IF EXISTS public.ida_attributetype\
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

                    objs.append(AttributeType(**row))

                AttributeType.objects.bulk_create(objs)
                self.logger.info('Created %s AttributeType instances', AttributeType.objects.count())
        else:
            self.logger.info('AttributeType data already exists')

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
                            ContentAttributes.objects.create(content_type=new_cte, attribute_type=atype)

            self.logger.info('Created %s ContentTypeExtended instances', ContentTypeExtended.objects.count())
        else:
            self.logger.info('ContentTypeExtended data already exists')

    @transaction.atomic
    def migrate_options_list(self):
        """Generate options list data."""
        if OptionsList.objects.count() == 0:
            self.logger.info('Migrating options lists')
            dalme_tenant = Tenant.objects.get(name='DALME').id
            gp_tenant = Tenant.objects.get(name='Global Pharmacopeias').id

            auth_list = OptionsList.objects.create(
                name='record authority',
                payload_type='static_list',
                description='List of authority sources for records.',
                creation_user_id=1,
                modification_user_id=1,
            )
            auth_list.values.create(
                tenant_id=dalme_tenant,
                payload=[
                    {'label': 'Chancery', 'value': 'Chancery'},
                    {'label': 'Church', 'value': 'Church'},
                    {'label': 'Court', 'value': 'Court'},
                    {'label': 'Notary', 'value': 'Notary'},
                ],
                creation_user_id=1,
                modification_user_id=1,
            )
            auth_list.values.create(
                tenant_id=dalme_tenant,
                payload=[
                    {'label': 'Chancery', 'value': 'Chancery'},
                    {'label': 'Church', 'value': 'Church'},
                    {'label': 'Court', 'value': 'Court'},
                    {'label': 'Notary', 'value': 'Notary'},
                ],
                creation_user_id=1,
                modification_user_id=1,
            )
            authority = AttributeType.objects.get(name='authority')
            authority.options = auth_list
            authority.save(update_fields=['options'])

            format_list = OptionsList.objects.create(
                name='record format',
                payload_type='static_list',
                description='List of formats for records.',
            )
            format_list.values.create(
                tenant_id=dalme_tenant,
                payload=[
                    {'label': 'Charter', 'value': 'Charter'},
                    {'label': 'Register - demi-quarto', 'value': 'Register - demi-quarto'},
                    {'label': 'Register - quarto', 'value': 'Register - quarto'},
                ],
                creation_user_id=1,
                modification_user_id=1,
            )
            att_format = AttributeType.objects.get(name='format')
            att_format.options = format_list
            att_format.save(update_fields=['options'])

            record_type_list = OptionsList.objects.create(
                name='record types',
                payload_type='static_list',
                description='List of record types.',
                creation_user_id=1,
                modification_user_id=1,
            )
            record_type_list.values.create(
                tenant_id=dalme_tenant,
                payload=[
                    {'label': 'Inventory-Comanda', 'value': 'Inventory-Comanda', 'group': 'Inventory'},
                    {
                        'label': 'Inventory-Criminal Inquest',
                        'value': 'Inventory-Criminal Inquest',
                        'group': 'Inventory',
                    },
                    {'label': 'Inventory-Custody', 'value': 'Inventory-Custody', 'group': 'Inventory'},
                    {'label': 'Inventory-Division', 'value': 'Inventory-Division', 'group': 'Inventory'},
                    {'label': 'Inventory-Donation', 'value': 'Inventory-Donation', 'group': 'Inventory'},
                    {'label': 'Inventory-Dowry', 'value': 'Inventory-Dowry', 'group': 'Inventory'},
                    {
                        'label': 'Inventory-Dowry Restitution',
                        'value': 'Inventory-Dowry Restitution',
                        'group': 'Inventory',
                    },
                    {'label': 'Inventory-Ecclesiastical', 'value': 'Inventory-Ecclesiastical', 'group': 'Inventory'},
                    {'label': 'Inventory-Emancipation', 'value': 'Inventory-Emancipation', 'group': 'Inventory'},
                    {'label': 'Inventory-Generic', 'value': 'Inventory-Generic', 'group': 'Inventory'},
                    {'label': 'Inventory-Guardianship', 'value': 'Inventory-Guardianship', 'group': 'Inventory'},
                    {'label': 'Inventory-Insolvency', 'value': 'Inventory-Insolvency', 'group': 'Inventory'},
                    {'label': 'Inventory-Legacy', 'value': 'Inventory-Legacy', 'group': 'Inventory'},
                    {'label': 'Inventory-List of objects', 'value': 'Inventory-List of objects', 'group': 'Inventory'},
                    {'label': 'Inventory-Postmortem', 'value': 'Inventory-Postmortem', 'group': 'Inventory'},
                    {'label': 'Inventory-Premortem', 'value': 'Inventory-Premortem', 'group': 'Inventory'},
                    {'label': 'Inventory-Probate', 'value': 'Inventory-Probate', 'group': 'Inventory'},
                    {'label': 'Inventory-Quittance', 'value': 'Inventory-Quittance', 'group': 'Inventory'},
                    {
                        'label': 'Inventory-Repudiation of inheritance',
                        'value': 'Inventory-Repudiation of inheritance',
                        'group': 'Inventory',
                    },
                    {
                        'label': 'Inventory-Restitution of pawned goods',
                        'value': 'Inventory-Restitution of pawned goods',
                        'group': 'Inventory',
                    },
                    {'label': 'Inventory-Ship', 'value': 'Inventory-Ship', 'group': 'Inventory'},
                    {
                        'label': 'Inventory-Taking up inheritance',
                        'value': 'Inventory-Taking up inheritance',
                        'group': 'Inventory',
                    },
                    {'label': 'Inventory-Tax seizure', 'value': 'Inventory-Tax seizure', 'group': 'Inventory'},
                    {
                        'label': 'Inventory-Undefended Goods',
                        'value': 'Inventory-Undefended Goods',
                        'group': 'Inventory',
                    },
                    {'label': 'Account Book-Household', 'value': 'Account Book-Household', 'group': 'Account Book'},
                    {'label': 'Account Book-Commercial', 'value': 'Account Book-Commercial', 'group': 'Account Book'},
                    {
                        'label': 'Account Book-Ecclesiastical',
                        'value': 'Account Book-Ecclesiastical',
                        'group': 'Account Book',
                    },
                    {'label': 'Account Book-Other', 'value': 'Account Book-Other', 'group': 'Account Book'},
                    {'label': 'Guardianship', 'value': 'Guardianship', 'group': 'Guardianship'},
                    {
                        'label': 'Liquidation of guardianship',
                        'value': 'Liquidation of guardianship',
                        'group': 'Guardianship',
                    },
                    {'label': 'Failed Seizure', 'value': 'Failed Seizure', 'group': 'Seizure'},
                    {'label': 'Seizure', 'value': 'Seizure', 'group': 'Seizure'},
                    {'label': 'Seizure-Debt', 'value': 'Seizure-Debt', 'group': 'Seizure'},
                    {'label': 'Seizure-Confiscation', 'value': 'Seizure-Confiscation', 'group': 'Seizure'},
                    {'label': 'Testament', 'value': 'Testament', 'group': 'Testament'},
                    {'label': 'Testamentary execution', 'value': 'Testamentary execution', 'group': 'Testament'},
                    {'label': 'Sale-Auction', 'value': 'Sale-Auction', 'group': 'Sales'},
                    {'label': 'Sale-Notarial', 'value': 'Sale-Notarial', 'group': 'Sales'},
                    {'label': 'Sale-Account', 'value': 'Sale-Account', 'group': 'Sales'},
                    {'label': 'Estimate-Dowry', 'value': 'Estimate-Dowry', 'group': 'Estimates'},
                    {'label': 'Estimate-Testament', 'value': 'Estimate-Testament', 'group': 'Estimates'},
                    {'label': 'Estimate-Insolvency', 'value': 'Estimate-Insolvency', 'group': 'Estimates'},
                    {'label': 'Estimate-Pledge', 'value': 'Estimate-Pledge', 'group': 'Estimates'},
                    {'label': 'Estimate-Investment', 'value': 'Estimate-Investment', 'group': 'Estimates'},
                    {'label': 'Estimate-Theft', 'value': 'Estimate-Theft', 'group': 'Estimates'},
                    {'label': 'Tariffs-Price Caps', 'value': 'Tariffs-Price Caps', 'group': 'Tariffs'},
                    {'label': 'Tariffs-Lists', 'value': 'Tariffs-Lists', 'group': 'Tariffs'},
                    {'label': 'Tariffs-Customs Registers', 'value': 'Tariffs-Customs Registers', 'group': 'Tariffs'},
                    {'label': 'Arrest', 'value': 'Arrest', 'group': 'Other'},
                    {'label': 'Auction', 'value': 'Auction', 'group': 'Other'},
                    {'label': 'Codicil', 'value': 'Codicil', 'group': 'Other'},
                    {'label': 'Eviction', 'value': 'Eviction', 'group': 'Other'},
                    {'label': 'Incarceration', 'value': 'Incarceration', 'group': 'Other'},
                    {'label': 'Object List-Fictional', 'value': 'Object List-Fictional', 'group': 'Other'},
                    {'label': 'Order to deliver goods', 'value': 'Order to deliver goods', 'group': 'Other'},
                    {'label': 'Promise to pay debt', 'value': 'Promise to pay debt', 'group': 'Other'},
                    {'label': 'Renvoi', 'value': 'Renvoi', 'group': 'Other'},
                    {'label': 'unclear', 'value': 'unclear', 'group': 'Other'},
                ],
                creation_user_id=1,
                modification_user_id=1,
            )
            record_type_list.values.create(
                tenant_id=gp_tenant,
                payload=[
                    {'label': 'Pharmacopeia-Functional', 'value': 'Pharmacopeia-Functional', 'group': 'Pharmacopeia'},
                    {'label': 'Pharmacopeia-Reference', 'value': 'Pharmacopeia-Reference', 'group': 'Pharmacopeia'},
                ],
                creation_user_id=1,
                modification_user_id=1,
            )
            record_type = AttributeType.objects.get(name='record_type')
            record_type.options = record_type_list
            record_type.save(update_fields=['options'])

            support_list = OptionsList.objects.create(
                name='record support',
                payload_type='static_list',
                description='List of support types for records.',
                creation_user_id=1,
                modification_user_id=1,
            )
            support_list.values.create(
                tenant_id=dalme_tenant,
                payload=[
                    {'label': 'Hybrid', 'value': 'Hybrid'},
                    {'label': 'Paper', 'value': 'Paper'},
                    {'label': 'Parchment', 'value': 'Parchment'},
                    {'label': 'Vellum', 'value': 'Vellum'},
                ],
                creation_user_id=1,
                modification_user_id=1,
            )
            support_list.values.create(
                tenant_id=gp_tenant,
                payload=[
                    {'label': 'Hybrid', 'value': 'Hybrid'},
                    {'label': 'Paper', 'value': 'Paper'},
                    {'label': 'Parchment', 'value': 'Parchment'},
                    {'label': 'Vellum', 'value': 'Vellum'},
                ],
                creation_user_id=1,
                modification_user_id=1,
            )
            support = AttributeType.objects.get(name='support')
            support.options = support_list
            support.save(update_fields=['options'])

            rights_status_list = OptionsList.objects.create(
                name='rights status',
                payload_type='static_list',
                description='List of valid status values for rights policies.',
                creation_user_id=1,
                modification_user_id=1,
            )
            rights_status_list.values.create(
                tenant_id=dalme_tenant,
                payload=[
                    {'label': 'Copyrighted', 'value': 'Copyrighted'},
                    {'label': 'Orphaned', 'value': 'Orphaned'},
                    {'label': 'Owned', 'value': 'Owned'},
                    {'label': 'Public Domain', 'value': 'Public Domain'},
                ],
                creation_user_id=1,
                modification_user_id=1,
            )
            rights_status_list.values.create(
                tenant_id=gp_tenant,
                payload=[
                    {'label': 'Copyrighted', 'value': 'Copyrighted'},
                    {'label': 'Orphaned', 'value': 'Orphaned'},
                    {'label': 'Owned', 'value': 'Owned'},
                    {'label': 'Public Domain', 'value': 'Public Domain'},
                ],
                creation_user_id=1,
                modification_user_id=1,
            )
            rights_status = AttributeType.objects.get(name='rights_status')
            rights_status.options = rights_status_list
            rights_status.save(update_fields=['options'])

            user_list = OptionsList.objects.create(
                name='full user list',
                payload_type='db_records',
                description='Full list of active system users.',
                creation_user_id=1,
                modification_user_id=1,
            )
            user_list.values.create(
                tenant_id=dalme_tenant,
                payload={
                    'app': 'auth',
                    'model': 'User',
                    'filters': {'is_active': True},
                    'concordance': {
                        'label': 'profile.full_name',
                        'value': 'id',
                        'detail': 'username',
                    },
                },
                creation_user_id=1,
                modification_user_id=1,
            )
            user_list.values.create(
                tenant_id=gp_tenant,
                payload={
                    'app': 'auth',
                    'model': 'User',
                    'filters': {'is_active': True},
                    'concordance': {
                        'label': 'profile.full_name',
                        'value': 'id',
                        'detail': 'username',
                    },
                },
                creation_user_id=1,
                modification_user_id=1,
            )
            owner = AttributeType.objects.get(name='owner')
            owner.options = user_list
            owner.save(update_fields=['options'])

            rights_status_list = OptionsList.objects.create(
                name='rights status list',
                payload_type='field_choices',
                description='List of possible status values for rights policies.',
                creation_user_id=1,
                modification_user_id=1,
            )
            rights_status_list.values.create(
                tenant_id=dalme_tenant,
                payload={
                    'app': 'ida',
                    'model': 'RightsPolicy',
                    'choices': 'RIGHTS_STATUS',
                },
                creation_user_id=1,
                modification_user_id=1,
            )
            rights_status_list.values.create(
                tenant_id=gp_tenant,
                payload={
                    'app': 'ida',
                    'model': 'RightsPolicy',
                    'choices': 'RIGHTS_STATUS',
                },
                creation_user_id=1,
                modification_user_id=1,
            )
            rights_status = AttributeType.objects.get(name='rights_status')
            rights_status.options = rights_status_list
            rights_status.save(update_fields=['options'])

            # TODO: Attention @gpizzorno do you want to do anything about these?
            # type options for Publication

            # type options for Organization

            # type for Location?

            self.logger.info('Created %s OptionsList instances', OptionsList.objects.count())
        else:
            self.logger.info('OptionsList data already exists')
