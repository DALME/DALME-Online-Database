"""Migrate the attributes."""

import json
from collections import Counter

from django.contrib.contenttypes.models import ContentType

# from django.contrib.auth import get_user_model
from django.db import connection, transaction

from ida.models import (
    Attribute,
    AttributeType,
    AttributeValueDate,
    AttributeValueDec,
    AttributeValueFkey,
    AttributeValueInt,
    AttributeValueJson,
    AttributeValueStr,
    AttributeValueTxt,
    ContentAttributes,
    User,
)

from .base import BaseStage


class Stage(BaseStage):
    """Data migration for attributes."""

    name = '06 Attributes'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.migrate_attributes()
        self.migrate_unused_attribute_types()

    @transaction.atomic
    def migrate_attributes(self):  # noqa: C901
        """Copy object attribute data.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0009_data_m_attributes.py#L5

        """
        if Attribute.objects.count() == 0:
            stats = Counter(
                {
                    'DATE': 0,
                    'DEC': 0,
                    'INT': 0,
                    'JSON': 0,
                    'TXT': 0,
                    'FKEY': 0,
                    'STR': 0,
                }
            )

            with connection.cursor() as cursor:
                self.logger.info('Migrating attributes')
                cursor.execute(
                    'SELECT attr.*, at.data_type FROM restore.core_attribute attr INNER JOIN restore.core_attribute_type at ON attr.attribute_type = at.id;'
                )
                rows = self.map_rows(cursor)

                for row in rows:
                    dtype = row.pop('data_type')
                    attribute_type_id = row.pop('attribute_type')
                    object_id = row.pop('object_id')
                    ctype = row.pop('content_type_id')
                    new_ctype = self.map_content_type(ctype, id_only=True)

                    value_date_d = row.pop('value_date_d')
                    value_date_m = row.pop('value_date_m')
                    value_date_y = row.pop('value_date_y')
                    value_date = row.pop('value_date')
                    value_json = row.pop('value_json')
                    value_str = row.pop('value_str')
                    value_dec = row.pop('value_dec')
                    value_int = row.pop('value_int')
                    value_txt = row.pop('value_txt')

                    if dtype == 'DATE':
                        AttributeValueDate.objects.create(
                            id=row['id'],
                            attribute_type_id=attribute_type_id,
                            object_id=object_id,
                            content_type_id=new_ctype,
                            day=value_date_d,
                            month=value_date_m,
                            year=value_date_y,
                            date=value_date,
                            text=value_str,
                            creation_user_id=row['creation_user_id'],
                            modification_user_id=row['modification_user_id'],
                            creation_timestamp=row['creation_timestamp'],
                            modification_timestamp=row['modification_timestamp'],
                        )

                    elif dtype == 'DEC':
                        AttributeValueDec.objects.create(
                            id=row['id'],
                            attribute_type_id=attribute_type_id,
                            object_id=object_id,
                            content_type_id=new_ctype,
                            value=value_dec,
                            creation_user_id=row['creation_user_id'],
                            modification_user_id=row['modification_user_id'],
                            creation_timestamp=row['creation_timestamp'],
                            modification_timestamp=row['modification_timestamp'],
                        )

                    elif dtype == 'INT':
                        AttributeValueInt.objects.create(
                            id=row['id'],
                            attribute_type_id=attribute_type_id,
                            object_id=object_id,
                            content_type_id=new_ctype,
                            value=value_int,
                            creation_user_id=row['creation_user_id'],
                            modification_user_id=row['modification_user_id'],
                            creation_timestamp=row['creation_timestamp'],
                            modification_timestamp=row['modification_timestamp'],
                        )

                    elif dtype == 'JSON':
                        AttributeValueJson.objects.create(
                            id=row['id'],
                            attribute_type_id=attribute_type_id,
                            object_id=object_id,
                            content_type_id=new_ctype,
                            value=value_json,
                            creation_user_id=row['creation_user_id'],
                            modification_user_id=row['modification_user_id'],
                            creation_timestamp=row['creation_timestamp'],
                            modification_timestamp=row['modification_timestamp'],
                        )

                    elif dtype == 'TXT':
                        AttributeValueTxt.objects.create(
                            id=row['id'],
                            attribute_type_id=attribute_type_id,
                            object_id=object_id,
                            content_type_id=new_ctype,
                            value=value_txt,
                            creation_user_id=row['creation_user_id'],
                            modification_user_id=row['modification_user_id'],
                            creation_timestamp=row['creation_timestamp'],
                            modification_timestamp=row['modification_timestamp'],
                        )

                    elif dtype in {'FK-UUID', 'FK-INT'}:
                        value_json = json.loads(value_json)
                        target_id = value_json['id'] if dtype == 'FK-UUID' else int(value_json['id'])
                        model = value_json['class'].lower()
                        obj_ct = ContentType.objects.get(app_label='ida', model=model)

                        AttributeValueFkey.objects.create(
                            id=row['id'],
                            attribute_type_id=attribute_type_id,
                            object_id=object_id,
                            content_type_id=new_ctype,
                            target_content_type=obj_ct,
                            target_id=target_id,
                            creation_user_id=row['creation_user_id'],
                            modification_user_id=row['modification_user_id'],
                            creation_timestamp=row['creation_timestamp'],
                            modification_timestamp=row['modification_timestamp'],
                        )
                        dtype = 'FKEY'  # Update this so the stats counter works correctly below.

                    elif dtype == 'STR':
                        AttributeValueStr.objects.create(
                            id=row['id'],
                            attribute_type_id=attribute_type_id,
                            object_id=object_id,
                            content_type_id=new_ctype,
                            value=value_str,
                            creation_user_id=row['creation_user_id'],
                            modification_user_id=row['modification_user_id'],
                            creation_timestamp=row['creation_timestamp'],
                            modification_timestamp=row['modification_timestamp'],
                        )

                    stats.update({dtype: 1})

                # https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0009_data_m_attributes.py#L170
                user_obj = User.objects.get(pk=1)
                for atype in AttributeType.objects.filter(data_type__in=['FK-UUID', 'FK-INT']):
                    atype.data_type = 'FKEY'
                    atype.modification_user = user_obj
                    atype.save()

                self.logger.info('Created %s Attribute instances', Attribute.objects.count())
                self.logger.info('Linked %s AttributeValue instances', stats.total())
                for key, value in stats.items():
                    self.logger.info('Total AttributeValue %s instances: %s', key, value)

        else:
            self.logger.info('Attribute data already exists')

    @transaction.atomic
    def migrate_unused_attribute_types(self):
        """Remove unused attribute types.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0012_data_m_atypes.py#L129

        """
        self.logger.info('Cleaning up unused attribute types')

        ct_count = ContentAttributes.objects.count()
        att_count = Attribute.objects.count()

        self.logger.info('%s attribute types are currently in use per CT count', ct_count)
        self.logger.info('%s attribute types are currently in use per ATT count', att_count)

        used_types_ct = {ct[0] for ct in ContentAttributes.objects.values_list('attribute_type__id')}
        used_types_att = {att[0] for att in Attribute.objects.values_list('attribute_type__id')}
        diff = used_types_ct.difference(used_types_att)

        if len(diff) > 0:
            self.logger.info(
                'The extra attribute types are: %s',
                ', '.join([a[0] for a in AttributeType.objects.filter(id__in=diff).values_list('name')]),
            )

        count = 0
        removed = []
        used_types = used_types_ct.union(used_types_att)

        for atype in AttributeType.objects.exclude(is_local=True, data_type='RREL'):
            if atype.id not in used_types:
                removed.append(atype.name)
                atype.delete()
                count += 1

        self.logger.info('Removed attribute types: %s', ', '.join(removed))
        self.logger.info('%s attribute types removed in total', count)
