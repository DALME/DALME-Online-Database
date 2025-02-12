"""Migrate Collection (from Set) and related models and data."""

from tqdm import tqdm

from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction

from domain.models import (
    Attribute,
    AttributeType,
    Collection,
    CollectionMembership,
    Permission,
    Record,
)
from oauth.models import User
from tenants.models import Tenant

from .base import BaseStage

WORKSET_TYPE = 4


class Stage(BaseStage):
    """Data migration for collections."""

    name = '11 Collections'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.migrate_collection()

    @transaction.atomic
    def migrate_collection(self):
        """Copy collection data.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0007_data_m_collections.py#L37

        """
        if Collection.objects.count() == 0:
            user_obj = User.objects.get(pk=1)
            collection_ct = ContentType.objects.get(app_label='domain', model='collection')
            group_ct = ContentType.objects.get(app_label='auth', model='group')
            record_ct = ContentType.objects.get(app_label='domain', model='record')
            tenant_id = Tenant.objects.get(name='DALME').id

            with connection.cursor() as cursor:
                self.logger.info('Migrating collections')
                cursor.execute('SELECT * FROM restore.core_set;')
                total = cursor.rowcount
                rows = self.map_rows(cursor)

                for row in tqdm(rows, total=total, desc='                     completed', leave=False):
                    row.pop('endpoint')
                    row.pop('has_landing')

                    row_id = row['id']
                    set_type = row.pop('set_type')
                    stat_text = row.pop('stat_text')
                    stat_title = row.pop('stat_title')
                    description = row.pop('description')
                    permissions = row.pop('permissions')
                    dataset_usergroup_id = row.pop('dataset_usergroup_id')

                    is_published = row.pop('is_public')
                    row.update(
                        {
                            'is_published': is_published,
                            'team_link_id': dataset_usergroup_id or None,
                            'tenant_id': tenant_id,
                            'use_as_workset': set_type == WORKSET_TYPE,
                        },
                    )

                    Collection.objects.create(**row)

                    if description:
                        Attribute.objects.create(
                            content_type=collection_ct,
                            object_id=row_id,
                            attribute_type=AttributeType.objects.get(name='description'),
                            value=description,
                            creation_user_id=1,
                            modification_user_id=1,
                        )

                    if stat_title is not None and stat_text is not None:
                        Attribute.objects.create(
                            content_type=collection_ct,
                            object_id=row_id,
                            attribute_type=AttributeType.objects.get(name='collection_metadata'),
                            value={stat_title: stat_text},
                            creation_user_id=1,
                            modification_user_id=1,
                        )

                    # Workset tracking.
                    cursor.execute('SELECT * FROM restore.core_set_x_content WHERE set_id_id = %s;', [row_id])
                    members = self.map_rows(cursor)

                    if set_type == WORKSET_TYPE:
                        workset_progress = [str(member['object_id']) for member in members if member['workset_done']]

                        Attribute.objects.create(
                            content_type=collection_ct,
                            object_id=row_id,
                            attribute_type=AttributeType.objects.get(name='workset_progress'),
                            value=workset_progress,
                            creation_user_id=1,
                            modification_user_id=1,
                        )

                    for member in members:
                        CollectionMembership.objects.create(
                            collection_id=row_id,
                            content_type=record_ct,
                            object_id=Record.objects.get(pk=member['object_id']).id,
                            tenant_id=tenant_id,
                            creation_user=User.objects.get(pk=member['creation_user_id']),
                            modification_user=User.objects.get(pk=member['modification_user_id']),
                            creation_timestamp=member['creation_timestamp'],
                            modification_timestamp=member['modification_timestamp'],
                        )

                    # 1. Default permissions.
                    Permission.objects.create(
                        content_type=collection_ct,
                        object_id=row_id,
                        is_default=True,
                        can_view=permissions != 1,
                        can_add=permissions not in [1, 2],
                        can_remove=permissions == 4,  # noqa: PLR2004
                        creation_user=user_obj,
                        modification_user=user_obj,
                    )

                    # 2. Permissions by dataset_usergroup (and user?).
                    if dataset_usergroup_id is not None:
                        Permission.objects.create(
                            content_type=collection_ct,
                            object_id=row_id,
                            principal_type=group_ct,
                            principal_id=dataset_usergroup_id,
                            can_view=True,
                            can_add=True,
                            can_remove=True,
                            creation_user=user_obj,
                            modification_user=user_obj,
                        )

                    # Omitted the comments handling, see the finalize stage.
                    # https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0007_data_m_collections.py#L159

            self.logger.info('Created %s Collection instances', Collection.objects.count())
        else:
            self.logger.warning('Collection data already exists')
