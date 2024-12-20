"""Migrate the attributes."""

import json
from collections import Counter

from django.apps import apps

# from django.contrib.auth import get_user_model
from django.db import connection, transaction

from domain.historical_date import HistoricalDate
from domain.models import Attribute, AttributeType, ContentAttributes, RecordType

from .base import BaseStage

RECORD_TYPE_COVERSIONS = {
    'Account Book-Other': 'Account Book',
    'Liquidation of guardianship': 'Guardianship-Liquidation',
    'Failed Seizure': 'Seizure-Failed',
    'Testamentary execution': 'Testament-Execution',
    'Object List-Fictional': 'Fictional object list',
    'unclear': 'Unclear',
    'Dowry': 'Inventory-Dowry',
}

ATYPES_KEEP = [
    'title',
    'language_gc',
    'creation_user',
    'modification_user',
    'author',
    'dam_user',
    'dam_id',
    'order',
    'ref',
    'creation_date',
    'file_size',
    'source',
    'data_type',
    'same_as',
    'options_list',
    'status',
    'result',
    'date_done',
    'subject',
    'file',
    'parents',
    'help_flag',
    'last_modified',
    'last_user',
    'activity',
    'endpoint',
    'progress',
    'is_published',
    'collection_metadata',
    'workset_progress',
    'corpus',
    'collection',
]


class Stage(BaseStage):
    """Data migration for attributes."""

    name = '07 Attributes'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.migrate_attributes()
        self.remove_unused_attribute_types()

    @transaction.atomic
    def migrate_attributes(self):  # noqa: C901, PLR0915
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

                # ids to manage exceptions:
                record_type_atype = AttributeType.objects.get(name='record_type')

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

                    # handle exceptions first, then process by data type
                    if attribute_type_id == record_type_atype.id:
                        label = RECORD_TYPE_COVERSIONS.get(value_str, value_str)
                        parent, name = label.split('-') if '-' in label else (None, None)

                        try:
                            if name and parent:
                                rt_obj = RecordType.objects.get(name=name, parent__name=parent)
                            else:
                                rt_obj = RecordType.objects.get(name=label, parent__isnull=True)

                        except RecordType.DoesNotExist:
                            rt_obj = None
                            self.logger.error('Failed to match record type: %s', value_str)  # noqa: TRY400

                        except RecordType.MultipleObjectsReturned:
                            rt_obj = None
                            self.logger.error('Found multiple record types for: %s', value_str)  # noqa: TRY400

                        if rt_obj:
                            payload['value'] = rt_obj
                            dtype = 'FKEY'  # Update so the stats counter works correctly below.
                        else:
                            continue

                    elif dtype == 'DATE':
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
                        model = apps.get_model(app_label='domain', model_name=model_name)
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

        used_types_ct = {ct[0] for ct in ContentAttributes.objects.values_list('attribute_type__id')}
        used_types_att = {att[0] for att in Attribute.objects.values_list('attribute_type__id')}

        self.logger.debug('%s attribute types are currently in use per CT count', len(used_types_ct))
        self.logger.debug('%s attribute types are currently in use per ATT count', len(used_types_att))

        count = 0
        removed = []
        used_types = used_types_ct.union(used_types_att)

        for atype in AttributeType.objects.exclude(is_local=True, data_type='RREL'):
            if atype.id not in used_types and atype.name not in ATYPES_KEEP:
                removed.append(atype.name)
                atype.delete()
                count += 1

        self.logger.info('Removed %s unused attribute types.', count)
