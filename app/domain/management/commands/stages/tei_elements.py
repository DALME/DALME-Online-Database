"""Migrate TEI elements."""

from django.db import transaction

from domain.models import Element, ElementAttribute, ElementSet, ElementSetMembership, OptionsList, Project
from tenants.models import Tenant

from .base import BaseStage
from .fixtures import TEI_ATTRIBUTE_OPTIONS, TEI_ELEMENTS


class Stage(BaseStage):
    """Data migration for attributes."""

    name = '15 TEI Elements'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.create_elements()

    @transaction.atomic
    def create_elements(self):
        """Create TEI elements."""
        if Element.objects.count() == 0:
            # create options
            self.logger.info('Creating element attribute options')
            tenant = Tenant.objects.get(name='IDA').id
            options_concordance = {}

            for opt in TEI_ATTRIBUTE_OPTIONS:
                options_list = OptionsList.objects.create(
                    name=opt['name'],
                    payload_type=opt['payload_type'],
                    description=opt['description'],
                    creation_user_id=1,
                    modification_user_id=1,
                )
                options_list.values.create(
                    tenant_id=tenant,
                    payload=opt['payload'],
                    public=False,
                    creation_user_id=1,
                    modification_user_id=1,
                )
                options_concordance[opt['key']] = options_list.id
                self.logger.debug('Created list: %s', opt['name'])

            # create default DALME element set
            self.logger.info('Creating default DALME element set')
            project = Project.objects.get(name='DALME')
            dalme_set = ElementSet.objects.create(
                label='DALME Default',
                description='Default TEI element set for the DALME project.',
                project=project,
                creation_user_id=1,
                modification_user_id=1,
                is_default=True,
            )

            # create elements
            self.logger.info('Creating TEI elements')
            for section in TEI_ELEMENTS:
                section_name = section['id']
                for item in section['items']:
                    attributes = item.pop('attributes', None)
                    in_context_menu = item.pop('in_context_menu', False)
                    in_toolbar = item.pop('in_toolbar', False)
                    item.update(
                        {
                            'section': section_name,
                            'creation_user_id': 1,
                            'modification_user_id': 1,
                        }
                    )
                    element = Element.objects.create(**item)
                    if attributes:
                        for att in attributes:
                            att['element_id'] = element.id
                            options = att.pop('options', None)
                            if options:
                                att['options_id'] = options_concordance[options]
                            ElementAttribute.objects.create(**att)

                    # add element to DALME set
                    ElementSetMembership.objects.create(
                        element_set=dalme_set,
                        element=element,
                        in_context_menu=in_context_menu,
                        in_toolbar=in_toolbar,
                    )

                    self.logger.debug('Created element: %s', item['label'])

        else:
            self.logger.warning('TEI data already exists')
