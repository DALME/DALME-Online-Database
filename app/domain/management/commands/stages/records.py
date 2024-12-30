"""Migrate Record (from Source)."""

from tqdm import tqdm

from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction

from domain.models import (
    Attribute,
    AttributeType,
    Organization,
    PageNode,
    Permission,
    Publication,
    Record,
    RecordGroup,
    Workflow,
    WorkLog,
)
from oauth.models import User

from .base import BaseStage

# dalme=# select distinct ct.name from restore.core_source s inner join restore.core_content_type ct on s.type = ct.id;
# -[ RECORD 1 ]----------
# name | Book section
# -[ RECORD 2 ]----------
# name | Manuscript
# -[ RECORD 3 ]----------
# name | Article
# -[ RECORD 4 ]----------
# name | Edited Book
# -[ RECORD 5 ]----------
# name | Book
# -[ RECORD 6 ]----------
# name | Academic article
# -[ RECORD 7 ]----------
# name | Archive
# -[ RECORD 8 ]----------
# name | Record
# -[ RECORD 9 ]----------
# name | File unit


ARCHIVE_TYPE_ID = 19
PUBLICATION_TYPE_IDS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11}
RECORD_GROUP_TYPE_ID = 12
NON_RECORD_IDS = [ARCHIVE_TYPE_ID, RECORD_GROUP_TYPE_ID, *PUBLICATION_TYPE_IDS]


class Stage(BaseStage):
    """Data migration for records."""

    name = '08 Records'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.migrate_record()
        self.migrate_page_nodes()
        self.migrate_worklog()
        self.migrate_workflow()

    @transaction.atomic
    def migrate_record(self):
        """Copy record data.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0008_data_m_misc.py#L5
        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0013_data_m_local_values.py#L5
        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0010_data_m_basic_types.py#L72
        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0010_data_m_basic_types.py#L118
        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0010_data_m_basic_types.py#L163

        """
        if Record.objects.count() == 0:
            user_obj = User.objects.get(pk=1)
            rg_ct = ContentType.objects.get(app_label='domain', model='recordgroup')
            org_ct = ContentType.objects.get(app_label='domain', model='organization')
            pub_ct = ContentType.objects.get(app_label='domain', model='publication')
            group_ct = ContentType.objects.get(app_label='auth', model='group')
            record_ct = ContentType.objects.get(app_label='domain', model='record')
            has_inv_type = AttributeType.objects.get(name='has_inventory')
            rec_count = 0

            with connection.cursor() as cursor:
                self.logger.info('Migrating records')
                cursor.execute(
                    'SELECT s.*, parent.type AS parent_type_id\
                        FROM restore.core_source s\
                        LEFT JOIN restore.core_source parent\
                        ON s.parent_id = parent.id;',
                )
                total = cursor.rowcount
                rows = self.map_rows(cursor)

                for row in tqdm(rows, total=total):
                    record_id = row['id']
                    type_id = row.pop('type')
                    is_private = row.pop('is_private')
                    has_inventory = row.pop('has_inventory')
                    primary_dataset_id = row.pop('primary_dataset_id')

                    # update parent record type
                    parent_type_id = row.pop('parent_type_id')
                    new_parent_type_id = self.map_content_type(parent_type_id, id_only=True)
                    row.update({'parent_type_id': new_parent_type_id})

                    # https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0010_data_m_basic_types.py#L72
                    if type_id not in NON_RECORD_IDS:
                        # self.logger.info('Creating record %s of type %s as Record', record_id, type_id)
                        Record.objects.create(**row)

                        if is_private:
                            Permission.objects.create(
                                content_type=record_ct,
                                object_id=record_id,
                                is_default=True,
                                can_view=False,
                                creation_user=user_obj,
                                modification_user=user_obj,
                            )
                        elif primary_dataset_id is not None:
                            cursor.execute(
                                'SELECT dataset_usergroup_id FROM restore.core_set WHERE id = %s;',
                                [primary_dataset_id],
                            )
                            ds_group_id = cursor.fetchone()[0]
                            Permission.objects.create(
                                content_type=record_ct,
                                object_id=record_id,
                                principal_type=group_ct,
                                principal_id=ds_group_id,
                                can_view=True,
                                can_edit=True,
                                creation_user=user_obj,
                                modification_user=user_obj,
                            )

                        Attribute.objects.create(
                            content_type=record_ct,
                            object_id=record_id,
                            attribute_type=has_inv_type,
                            value=has_inventory,
                            creation_user_id=row['creation_user_id'],
                            modification_user_id=row['modification_user_id'],
                            creation_timestamp=row['creation_timestamp'],
                            modification_timestamp=row['modification_timestamp'],
                        )

                        rec_count += 1

                    else:
                        if type_id == ARCHIVE_TYPE_ID:
                            # self.logger.info('Creating record %s of type %s as Organization', record_id, type_id)
                            new_ct = org_ct
                            Organization.objects.create(
                                id=record_id,
                                name=row['name'],
                                agent_type=2,
                                short_name=row['short_name'],
                                creation_user_id=row['creation_user_id'],
                                modification_user_id=row['modification_user_id'],
                                creation_timestamp=row['creation_timestamp'],
                                modification_timestamp=row['modification_timestamp'],
                            )

                        # https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0010_data_m_basic_types.py#L118
                        elif type_id in PUBLICATION_TYPE_IDS:
                            # self.logger.info('Creating record %s of type %s as Publication', record_id, type_id)
                            new_ct = pub_ct
                            Publication.objects.create(
                                id=record_id,
                                name=row['name'],
                                short_name=row['short_name'],
                                creation_user_id=row['creation_user_id'],
                                modification_user_id=row['modification_user_id'],
                                creation_timestamp=row['creation_timestamp'],
                                modification_timestamp=row['modification_timestamp'],
                            )

                        # https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0010_data_m_basic_types.py#L163
                        elif type_id == RECORD_GROUP_TYPE_ID:
                            # self.logger.info('Creating record %s of type %s as RecordGroup', record_id, type_id)
                            new_ct = rg_ct
                            RecordGroup.objects.create(**row)

                        for att in Attribute.objects.filter(content_type=record_ct, object_id=record_id):
                            att.content_type = new_ct
                            att.save(update_fields=['content_type'])

                        rec_count += 1

            self.logger.info('Created %s Record instances', rec_count)
        else:
            self.logger.warning('Record data already exists')

    @transaction.atomic
    def migrate_page_nodes(self):
        """Copy source_page data to PageNode."""
        if PageNode.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating page nodes')
                cursor.execute('SELECT * FROM restore.core_source_pages;')
                rows = self.map_rows(cursor)
                objs = []
                for row in rows:
                    record_id = row.pop('source_id')
                    row.update({'record_id': record_id})
                    objs.append(PageNode(**row))

                PageNode.objects.bulk_create(objs)
                self.logger.info('Created %s node instances', PageNode.objects.count())
        else:
            self.logger.warning('PageNode data already exists')

    @transaction.atomic
    def migrate_worklog(self):
        """Copy worklog data."""
        if WorkLog.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating worklogs')
                cursor.execute('SELECT * FROM restore.core_work_log;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    record_id = row.pop('source_id')
                    row.update({'record_id': record_id})
                    objs.append(WorkLog(**row))

                WorkLog.objects.bulk_create(objs)
                self.logger.info('Created %s WorkLog instances', WorkLog.objects.count())
        else:
            self.logger.warning('WorkLog data already exists')

    @transaction.atomic
    def migrate_workflow(self):
        """Copy workflow data."""
        if Workflow.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating workflows')
                cursor.execute('SELECT * FROM restore.core_workflow;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    record_id = row.pop('source_id')
                    row.update({'record_id': record_id})
                    objs.append(Workflow(**row))

                Workflow.objects.bulk_create(objs)
                self.logger.info('Created %s Workflow instances', Workflow.objects.count())
        else:
            self.logger.warning('Workflow data already exists')
