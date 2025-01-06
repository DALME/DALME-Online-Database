"""Migrate TEI elements."""

from django.db import transaction

from domain.models import Element, ElementAttribute, ElementSet, OptionsList, Project
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
        self.create_default_project_set()

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

            # create elements
            self.logger.info('Creating TEI elements')
            for section in TEI_ELEMENTS:
                section_name = section['id']
                for item in section['items']:
                    attributes = item.pop('attributes', None)
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
                    self.logger.debug('Created element: %s', item['label'])

        else:
            self.logger.warning('TEI data already exists')

    @transaction.atomic
    def create_default_project_set(self):
        """Create default TEI elements set for DALME project."""
        self.logger.info('Creating default TEI elements set for DALME project')
        project = Project.objects.get(name='DALME')
        elements = Element.objects.all()
        element_set = ElementSet.objects.create(
            content_object=project,
            is_default=True,
            description='Default TEI element set for DALME project.',
        )
        element_set.elements.add(*elements)
