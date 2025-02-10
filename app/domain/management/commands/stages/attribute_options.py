"""Generate options list data."""

from django.db import transaction

from domain.models import (
    AttributeType,
    OptionsList,
    RecordType,
)
from tenants.models import Tenant

from .base import BaseStage
from .fixtures import OPTIONS, RECORD_TYPES


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

            for tenant_name, types in RECORD_TYPES.items():
                tenant = Tenant.objects.get(name=tenant_name)

                for record_type in types:
                    parent = RecordType.objects.create(tenant=tenant, name=record_type['name'])
                    if record_type.get('subtypes'):
                        for subtype in record_type['subtypes']:
                            RecordType.objects.create(tenant=tenant, name=subtype, parent=parent)

                self.logger.info(
                    'Created %s RecordType instances for %s',
                    RecordType.objects.filter(tenant=tenant).count(),
                    tenant_name,
                )
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
