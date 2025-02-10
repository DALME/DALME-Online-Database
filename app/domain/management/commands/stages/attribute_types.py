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
from .fixtures import CT_DATA, CTA_PROPS, NEW_TYPES, RENAMES, TO_BOOL, TO_FKEY, TO_INT, TO_LOCAL, TO_RREL


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
