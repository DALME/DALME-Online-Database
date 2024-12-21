"""Generate options list data."""

from django.db import transaction

from domain.models import (
    AttributeType,
    OptionsList,
    RecordType,
)
from tenants.models import Tenant

from .base import BaseStage

OPTIONS = [
    {
        'atype_name': 'authority',
        'name': 'record authority',
        'payload_type': 'static_list',
        'description': 'List of authority sources for records.',
        'payload': [
            {'label': 'Chancery', 'value': 'Chancery'},
            {'label': 'Church', 'value': 'Church'},
            {'label': 'Court', 'value': 'Court'},
            {'label': 'Notary', 'value': 'Notary'},
        ],
        'pharma_schema': True,
    },
    {
        'atype_name': 'format',
        'name': 'record format',
        'payload_type': 'static_list',
        'description': 'List of formats for records.',
        'payload': [
            {'label': 'Charter', 'value': 'Charter'},
            {'label': 'Register - demi-quarto', 'value': 'Register - demi-quarto'},
            {'label': 'Register - quarto', 'value': 'Register - quarto'},
        ],
        'pharma_schema': False,
    },
    {
        'atype_name': 'record_type',
        'name': 'record types',
        'payload_type': 'db_records',
        'description': 'List of record types.',
        'payload': {
            'app': 'domain',
            'model': 'RecordType',
            'concordance': {'value': 'id'},
        },
        'pharma_schema': True,
    },
    {
        'atype_name': 'support',
        'name': 'record support',
        'payload_type': 'static_list',
        'description': 'List of support types for records.',
        'payload': [
            {'label': 'Hybrid', 'value': 'Hybrid'},
            {'label': 'Paper', 'value': 'Paper'},
            {'label': 'Parchment', 'value': 'Parchment'},
            {'label': 'Vellum', 'value': 'Vellum'},
        ],
        'pharma_schema': True,
    },
    {
        'atype_name': 'rights_status',
        'name': 'rights status',
        'payload_type': 'static_list',
        'description': 'List of valid status values for rights policies.',
        'payload': [
            {'label': 'Copyrighted', 'value': 'Copyrighted'},
            {'label': 'Orphaned', 'value': 'Orphaned'},
            {'label': 'Owned', 'value': 'Owned'},
            {'label': 'Public Domain', 'value': 'Public Domain'},
        ],
        'pharma_schema': True,
    },
    {
        'atype_name': 'owner',
        'name': 'full user list',
        'payload_type': 'db_records',
        'description': 'Full list of active system users.',
        'payload': {
            'app': 'auth',
            'model': 'User',
            'filters': {'is_active': True},
            'concordance': {
                'label': 'full_name',
                'value': 'id',
                'detail': 'username',
            },
        },
        'pharma_schema': True,
    },
    {
        'atype_name': 'rights_status',
        'name': 'rights status list',
        'payload_type': 'field_choices',
        'description': 'List of possible status values for rights policies.',
        'payload': {
            'app': 'domain',
            'model': 'RightsPolicy',
            'choices': 'RIGHTS_STATUS',
        },
        'pharma_schema': True,
    },
    {
        'atype_name': 'language',
        'name': 'full language list',
        'payload_type': 'db_records',
        'description': 'Full list of languages.',
        'payload': {
            'app': 'domain',
            'model': 'LanguageReference',
            'concordance': {
                'label': 'name',
                'value': 'id',
            },
        },
        'pharma_schema': True,
    },
    {
        'atype_name': 'country',
        'name': 'list of countries',
        'payload_type': 'db_records',
        'description': 'List of countries.',
        'payload': {
            'app': 'domain',
            'model': 'CountryReference',
            'concordance': {
                'label': 'name',
                'value': 'id',
            },
        },
        'pharma_schema': True,
    },
    {
        'atype_name': 'locale',
        'name': 'full locale list',
        'payload_type': 'db_records',
        'description': 'Full list of locales.',
        'payload': {
            'app': 'domain',
            'model': 'LocaleReference',
            'concordance': {
                'label': 'name',
                'value': 'id',
                'group': 'country',
            },
        },
        'pharma_schema': True,
    },
    {
        'atype_name': 'collection',
        'name': 'full collections list',
        'payload_type': 'db_records',
        'description': 'Full list of owned/non-private collections.',
        'payload': {
            'app': 'domain',
            'model': 'Collection',
            'filters': {'is_corpus': False},
            'concordance': {
                'label': 'name',
                'value': 'id',
                'group': 'team_link',
            },
        },
        'pharma_schema': True,
    },
    {
        'atype_name': 'collection',
        'name': 'public collections list',
        'payload_type': 'db_records',
        'description': 'Full list of owned/non-private collections.',
        'payload': {
            'app': 'domain',
            'model': 'Collection',
            'filters': {
                'is_corpus': False,
                'is_published': True,
            },
            'concordance': {
                'label': 'name',
                'value': 'id',
            },
        },
        'public': True,
        'pharma_schema': True,
    },
    {
        'atype_name': 'corpus',
        'name': 'corpora list',
        'payload_type': 'db_records',
        'description': 'Full list of corpora.',
        'payload': {
            'app': 'domain',
            'model': 'Collection',
            'filters': {'is_corpus': True},
            'concordance': {
                'label': 'name',
                'value': 'id',
            },
        },
        'pharma_schema': True,
    },
    {
        'atype_name': 'corpus',
        'name': 'public corpora list',
        'payload_type': 'db_records',
        'description': 'Full list of public corpora.',
        'payload': {
            'app': 'domain',
            'model': 'Collection',
            'filters': {
                'is_corpus': True,
                'is_published': True,
            },
            'concordance': {
                'label': 'name',
                'value': 'id',
            },
        },
        'public': True,
        'pharma_schema': True,
    },
]


class Stage(BaseStage):
    """Data migration for attribute options."""

    name = '06 Attribute Options'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.create_record_types()
        self.migrate_options_list()

    @transaction.atomic
    def create_record_types(self):
        """Create new record types."""
        if RecordType.objects.count() == 0:
            self.logger.info('Creating record types')

            dalme = Tenant.objects.get(name='DALME')
            gp = Tenant.objects.get(name='Pharmacopeias')

            inventory = RecordType.objects.create(tenant=dalme, name='Inventory')
            account_book = RecordType.objects.create(tenant=dalme, name='Account Book')
            guardianship = RecordType.objects.create(tenant=dalme, name='Guardianship')
            seizure = RecordType.objects.create(tenant=dalme, name='Seizure')
            testament = RecordType.objects.create(tenant=dalme, name='Testament')
            sales = RecordType.objects.create(tenant=dalme, name='Sale')
            estimates = RecordType.objects.create(tenant=dalme, name='Estimate')
            tariffs = RecordType.objects.create(tenant=dalme, name='Tariffs')

            subtypes = [
                RecordType(tenant=dalme, name='Comanda', parent=inventory),
                RecordType(tenant=dalme, name='Confiscation', parent=inventory),
                RecordType(tenant=dalme, name='Criminal Inquest', parent=inventory),
                RecordType(tenant=dalme, name='Custody', parent=inventory),
                RecordType(tenant=dalme, name='Division', parent=inventory),
                RecordType(tenant=dalme, name='Donation', parent=inventory),
                RecordType(tenant=dalme, name='Dowry', parent=inventory),
                RecordType(tenant=dalme, name='Dowry Restitution', parent=inventory),
                RecordType(tenant=dalme, name='Ecclesiastical', parent=inventory),
                RecordType(tenant=dalme, name='Emancipation', parent=inventory),
                RecordType(tenant=dalme, name='Generic', parent=inventory),
                RecordType(tenant=dalme, name='Guardianship', parent=inventory),
                RecordType(tenant=dalme, name='Insolvency', parent=inventory),
                RecordType(tenant=dalme, name='Legacy', parent=inventory),
                RecordType(tenant=dalme, name='List of objects', parent=inventory),
                RecordType(tenant=dalme, name='Postmortem', parent=inventory),
                RecordType(tenant=dalme, name='Premortem', parent=inventory),
                RecordType(tenant=dalme, name='Probate', parent=inventory),
                RecordType(tenant=dalme, name='Quittance', parent=inventory),
                RecordType(tenant=dalme, name='Repudiation of inheritance', parent=inventory),
                RecordType(tenant=dalme, name='Restitution of pawned goods', parent=inventory),
                RecordType(tenant=dalme, name='Ship', parent=inventory),
                RecordType(tenant=dalme, name='Taking up inheritance', parent=inventory),
                RecordType(tenant=dalme, name='Tax seizure', parent=inventory),
                RecordType(tenant=dalme, name='Tax assessment', parent=inventory),
                RecordType(tenant=dalme, name='Undefended Goods', parent=inventory),
                RecordType(tenant=dalme, name='Household', parent=account_book),
                RecordType(tenant=dalme, name='Commercial', parent=account_book),
                RecordType(tenant=dalme, name='Ecclesiastical', parent=account_book),
                RecordType(tenant=dalme, name='Liquidation', parent=guardianship),
                RecordType(tenant=dalme, name='Failed', parent=seizure),
                RecordType(tenant=dalme, name='Debt', parent=seizure),
                RecordType(tenant=dalme, name='Confiscation', parent=seizure),
                RecordType(tenant=dalme, name='Execution', parent=testament),
                RecordType(tenant=dalme, name='Auction', parent=sales),
                RecordType(tenant=dalme, name='Notarial', parent=sales),
                RecordType(tenant=dalme, name='Account', parent=sales),
                RecordType(tenant=dalme, name='Dowry', parent=estimates),
                RecordType(tenant=dalme, name='Testament', parent=estimates),
                RecordType(tenant=dalme, name='Insolvency', parent=estimates),
                RecordType(tenant=dalme, name='Pledge', parent=estimates),
                RecordType(tenant=dalme, name='Investment', parent=estimates),
                RecordType(tenant=dalme, name='Theft', parent=estimates),
                RecordType(tenant=dalme, name='Price Caps', parent=tariffs),
                RecordType(tenant=dalme, name='Lists', parent=tariffs),
                RecordType(tenant=dalme, name='Customs Registers', parent=tariffs),
                RecordType(tenant=dalme, name='Arrest'),
                RecordType(tenant=dalme, name='Auction'),
                RecordType(tenant=dalme, name='Codicil'),
                RecordType(tenant=dalme, name='Eviction'),
                RecordType(tenant=dalme, name='Incarceration'),
                RecordType(tenant=dalme, name='Fictional object list'),
                RecordType(tenant=dalme, name='Order to deliver goods'),
                RecordType(tenant=dalme, name='Promise to pay debt'),
                RecordType(tenant=dalme, name='Renvoi'),
                RecordType(tenant=dalme, name='Unclear'),
            ]

            RecordType.objects.bulk_create(subtypes)
            self.logger.info('Created %s RecordType instances for DALME', RecordType.objects.count())

            pharmacopeia = RecordType.objects.create(tenant=gp, name='Pharmacopeia')
            RecordType.objects.create(tenant=gp, name='Functional', parent=pharmacopeia)
            RecordType.objects.create(tenant=gp, name='Reference', parent=pharmacopeia)

            self.logger.info('Created %s RecordType instances for GP', RecordType.objects.filter(tenant=gp).count())
        else:
            self.logger.warning('RecordType data already exists')

    @transaction.atomic
    def migrate_options_list(self):
        """Generate options list data."""
        if OptionsList.objects.count() == 0:
            self.logger.info('Migrating options lists')
            dalme_tenant = Tenant.objects.get(name='DALME').id
            gp_tenant = Tenant.objects.get(name='Pharmacopeias').id

            for opt in OPTIONS:
                options_list = OptionsList.objects.create(
                    name=opt['name'],
                    payload_type=opt['payload_type'],
                    description=opt['description'],
                    creation_user_id=1,
                    modification_user_id=1,
                )
                options_list.values.create(
                    tenant_id=dalme_tenant,
                    payload=opt['payload'],
                    public=opt.get('public', False),
                    creation_user_id=1,
                    modification_user_id=1,
                )

                if opt['pharma_schema']:
                    options_list.values.create(
                        tenant_id=gp_tenant,
                        payload=opt['pharma_payload'] if opt.get('pharma_payload') else opt['payload'],
                        public=opt.get('public', False),
                        creation_user_id=1,
                        modification_user_id=1,
                    )

                atype_obj = AttributeType.objects.get(name=opt['atype_name'])
                atype_obj.options = options_list
                atype_obj.save(update_fields=['options'])

                self.logger.debug('Created options for %s', opt['atype_name'])

            self.logger.info('Created %s OptionsList instances', OptionsList.objects.count())
        else:
            self.logger.warning('OptionsList data already exists')
