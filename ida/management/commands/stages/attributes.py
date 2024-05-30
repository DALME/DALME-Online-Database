"""Migrate the attributes."""

import json
from collections import Counter

from django.apps import apps

# from django.contrib.auth import get_user_model
from django.db import connection, transaction

from ida.models import Attribute, AttributeType, ContentAttributes
from ida.models.utils import HistoricalDate

from .base import BaseStage


class Stage(BaseStage):
    """Data migration for attributes."""

    name = '06 Attributes'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.migrate_attributes()
        self.remove_unused_attribute_types()

    @transaction.atomic
    def migrate_attributes(self):
        """Copy object attribute data.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0009_data_m_attributes.py#L5

        """
        if Attribute.objects.count() == 0:
            stats = Counter(
                {
                    'DATE': 0,
                    'FLOAT': 0,
                    'INT': 0,
                    'JSON': 0,
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

                    payload = {
                        'id': row['id'],
                        'attribute_type_id': attribute_type_id,
                        'object_id': object_id,
                        'content_type_id': new_ctype,
                        'creation_user_id': row['creation_user_id'],
                        'modification_user_id': row['modification_user_id'],
                        'creation_timestamp': row['creation_timestamp'],
                        'modification_timestamp': row['modification_timestamp'],
                    }

                    if dtype == 'DATE':
                        payload['value'] = HistoricalDate(
                            {
                                'day': value_date_d,
                                'month': value_date_m,
                                'year': value_date_y,
                                'date': value_date,
                                'text': value_str,
                            }
                        )

                    elif dtype in ['DEC', 'FLOAT']:
                        payload['value'] = float(value_dec)
                        dtype = 'FLOAT'  # Update so the stats counter works correctly below.

                    elif dtype == 'INT':
                        payload['value'] = int(value_int)

                    elif dtype == 'JSON':
                        payload['value'] = json.loads(value_json)

                    elif dtype in ['TXT', 'STR']:
                        payload['value'] = value_txt if dtype == 'TXT' else value_str
                        dtype = 'STR'  # Update so the stats counter works correctly below.

                    elif dtype in ['FK-UUID', 'FK-INT']:
                        value_json = json.loads(value_json)
                        target_id = value_json['id'] if dtype == 'FK-UUID' else int(value_json['id'])
                        model_name = value_json['class'].lower()
                        model = apps.get_model(app_label='ida', model_name=model_name)
                        payload['value'] = model.objects.get(pk=target_id)
                        dtype = 'FKEY'  # Update so the stats counter works correctly below.

                    Attribute.objects.create(**payload)
                    stats.update({dtype: 1})

                self.logger.debug(
                    'Created %s Attribute instances, table count = %s', stats.total(), Attribute.objects.count()
                )
                for key, value in stats.items():
                    self.logger.debug('Total Attribute %s instances: %s', key, value)

        else:
            self.logger.warning('Attribute data already exists')

    @transaction.atomic
    def remove_unused_attribute_types(self):
        """Remove unused attribute types.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0012_data_m_atypes.py#L129

        """
        self.logger.info('Cleaning up unused attribute types')

        ct_count = ContentAttributes.objects.count()
        att_count = Attribute.objects.count()

        self.logger.debug('%s attribute types are currently in use per CT count', ct_count)
        self.logger.debug('%s attribute types are currently in use per ATT count', att_count)

        used_types_ct = {ct[0] for ct in ContentAttributes.objects.values_list('attribute_type__id')}
        used_types_att = {att[0] for att in Attribute.objects.values_list('attribute_type__id')}
        diff = used_types_ct.difference(used_types_att)

        if len(diff) > 0:
            self.logger.debug(
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

        self.logger.debug('Removed attribute types: %s', ', '.join(removed))
        self.logger.info('%s attribute types removed in total', count)
