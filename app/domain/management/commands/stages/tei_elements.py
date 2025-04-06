"""Migrate TEI elements."""

from django.db import transaction

from domain.models import (
    Element,
    ElementSet,
    ElementSetMembership,
    ElementTag,
    ElementTagAttribute,
    OptionsList,
    Project,
)
from tenants.models import Tenant

from .base import BaseStage
from .fixtures import TEI_ATTRIBUTE_OPTIONS, TEI_ELEMENTS


class Stage(BaseStage):
    """Data migration for attributes."""

    name = '14 TEI Elements'

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
            for element in TEI_ELEMENTS:
                tags = element.pop('tags', None)
                in_context_menu = element.pop('in_context_menu', False)
                in_toolbar = element.pop('in_toolbar', False)
                element.update(
                    {
                        'creation_user_id': 1,
                        'modification_user_id': 1,
                    }
                )

                element_object = Element.objects.create(**element)

                if tags:
                    tag_concordance = {}
                    for tag in tags:
                        attributes = tag.pop('attributes', None)
                        parent = tag.pop('parent', None)
                        tag['element_id'] = element_object.id
                        if parent:
                            tag['parent_id'] = tag_concordance[parent]

                        tag_object = ElementTag.objects.create(**tag)
                        tag_concordance[tag_object.name] = tag_object.id

                        if attributes:
                            for att in attributes:
                                options = att.pop('options', None)
                                if options:
                                    att['options_id'] = options_concordance[options]

                                att['tag_id'] = tag_object.id
                                ElementTagAttribute.objects.create(**att)

                # add element to DALME set
                ElementSetMembership.objects.create(
                    element_set=dalme_set,
                    element=element_object,
                    in_context_menu=in_context_menu,
                    in_toolbar=in_toolbar,
                )

        else:
            self.logger.warning('TEI data already exists')
