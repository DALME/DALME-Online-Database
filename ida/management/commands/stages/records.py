"""Migrate Record (from Source)."""
from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction

from dalme_app.models import Workflow, WorkLog
from ida.models import (
    Attribute,
    AttributeType,
    AttributeValueBool,
    Organization,
    Permission,
    Publication,
    Record,
    RecordGroup,
    Tenant,
    User,
)

from .base import BaseStage

# dalme=# select distinct ct.name from restore.dalme_app_source s inner join restore.dalme_app_content_type ct on s.type = ct.id;
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


class Stage(BaseStage):
    """Data migration for records."""

    name = '07 Records'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.migrate_record()
        self.migrate_worklog()
        self.migrate_workflow()

    @transaction.atomic
    def migrate_record(self):  # noqa: C901, PLR0915
        """Copy record data.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0008_data_m_misc.py#L5
        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0013_data_m_local_values.py#L5
        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0010_data_m_basic_types.py#L72
        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0010_data_m_basic_types.py#L118
        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0010_data_m_basic_types.py#L163

        """
        if Record.objects.count() == 0:
            user_obj = User.objects.get(pk=1)
            rg_ct = ContentType.objects.get(app_label='ida', model='recordgroup')
            org_ct = ContentType.objects.get(app_label='ida', model='organization')
            pub_ct = ContentType.objects.get(app_label='ida', model='publication')
            group_ct = ContentType.objects.get(app_label='auth', model='group')
            record_ct = ContentType.objects.get(app_label='ida', model='record')
            has_inv_type = AttributeType.objects.get(name='has_inventory')

            with connection.cursor() as cursor:
                self.logger.info('Migrating records')
                cursor.execute(
                    'SELECT s.*, ct.model AS parent_ct_model FROM restore.dalme_app_source s INNER JOIN restore.django_content_type ct ON s.type = ct.id;'
                )
                rows = self.map_rows(cursor)

                for row in rows:
                    record_id = row['id']
                    type_id = row.pop('type')
                    is_private = row.pop('is_private')
                    has_inventory = row.pop('has_inventory')
                    primary_dataset_id = row.pop('primary_dataset_id')

                    parent_ct_model = row.pop('parent_ct_model')

                    new_ct = self.map_content_type(type_id)
                    assert parent_ct_model == new_ct['model']
                    row.update({'parent_type_id': new_ct['id']})

                    record = Record.objects.create(**row)

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
                            'SELECT dataset_usergroup_id FROM restore.dalme_app_set WHERE id = %s;',
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

                    AttributeValueBool.objects.create(
                        content_type=record_ct,
                        object_id=record_id,
                        attribute_type=has_inv_type,
                        value=has_inventory,
                        creation_user_id=row['creation_user_id'],
                        modification_user_id=row['modification_user_id'],
                        creation_timestamp=row['creation_timestamp'],
                        modification_timestamp=row['modification_timestamp'],
                    )

                    # https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0010_data_m_basic_types.py#L72
                    if type_id == ARCHIVE_TYPE_ID:
                        self.logger.info('Coverting Record %s into Organization', record_id)
                        organization = Organization.objects.create(
                            id=record_id,
                            name=row['name'],
                            agent_type=2,
                            short_name=row['short_name'],
                            creation_user_id=row['creation_user_id'],
                            modification_user_id=row['modification_user_id'],
                            creation_timestamp=row['creation_timestamp'],
                            modification_timestamp=row['modification_timestamp'],
                        )

                        for att in Attribute.objects.filter(content_type=record_ct, object_id=record_id):
                            att.content_type = org_ct
                            att.save(update_fields=['content_type'])

                        for child in Record.objects.filter(parent_id=record_id):
                            child.parent_type = org_ct
                            child.parent_id = organization.id
                            child.save(update_fields=['parent_type', 'parent_id'])

                        record.delete()

                    # https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0010_data_m_basic_types.py#L118
                    if type_id in PUBLICATION_TYPE_IDS:
                        self.logger.info('Coverting Record %s into Publication', record_id)
                        publication = Publication.objects.create(
                            id=record_id,
                            name=row['name'],
                            short_name=row['short_name'],
                            creation_user_id=row['creation_user_id'],
                            modification_user_id=row['modification_user_id'],
                            creation_timestamp=row['creation_timestamp'],
                            modification_timestamp=row['modification_timestamp'],
                        )

                        for att in Attribute.objects.filter(content_type=record_ct, object_id=record_id):
                            att.content_type = pub_ct
                            att.save(update_fields=['content_type'])

                        for child in Record.objects.filter(parent_id=record_id):
                            child.parent_type = pub_ct
                            child.parent_id = publication.id
                            child.save(update_fields=['parent_type', 'parent_id'])

                        record.delete()

                    # https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0010_data_m_basic_types.py#L163
                    if type_id == RECORD_GROUP_TYPE_ID:
                        self.logger.info('Coverting Record %s into RecordGroup', record_id)
                        record_group = RecordGroup.objects.create(
                            id=record_id,
                            name=row['name'],
                            short_name=row['short_name'],
                            creation_user_id=row['creation_user_id'],
                            modification_user_id=row['modification_user_id'],
                            creation_timestamp=row['creation_timestamp'],
                            modification_timestamp=row['modification_timestamp'],
                        )

                        if record.parent_type:
                            record_group.parent_type = record.parent_type
                            record_group.parent_id = record.parent_id
                            record_group.save(update_fields=['parent_type', 'parent_id'])
                        elif record.parent_id:
                            parent_ct = ContentType.objects.get_for_model(record.parent)
                            record_group.parent_type = parent_ct
                            record_group.parent_id = record.parent.id
                            record_group.save(update_fields=['parent_type', 'parent_id'])

                        for att in Attribute.objects.filter(content_type=record_ct, object_id=record_id):
                            att.content_type = rg_ct
                            att.save(update_fields=['content_type'])

                        for child in Record.objects.filter(parent_id=record.id):
                            child.parent_type = rg_ct
                            child.parent_id = record_group.id
                            child.save(update_fields=['parent_type', 'parent_id'])

                        record.delete()

            self.logger.info('Created %s Record instances', Record.objects.count())
        else:
            self.logger.info('Record data already exists')

    @transaction.atomic
    def migrate_worklog(self):
        """Copy worklog data."""
        if WorkLog.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating worklogs')
                tenant_id = Tenant.objects.get(name='DALME').id
                cursor.execute('SELECT * FROM restore.dalme_app_work_log;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    record_id = row.pop('source_id')
                    row.update({'record_id': record_id, 'tenant_id': tenant_id})
                    objs.append(WorkLog(**row))

                WorkLog.objects.bulk_create(objs)
                self.logger.info('Created %s WorkLog instances', WorkLog.objects.count())
        else:
            self.logger.info('WorkLog data already exists')

    @transaction.atomic
    def migrate_workflow(self):
        """Copy workflow data."""
        if Workflow.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating workflows')
                tenant_id = Tenant.objects.get(name='DALME').id
                cursor.execute('SELECT * FROM restore.dalme_app_workflow;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    record_id = row.pop('source_id')
                    row.update({'record_id': record_id, 'tenant_id': tenant_id})
                    objs.append(Workflow(**row))

                Workflow.objects.bulk_create(objs)
                self.logger.info('Created %s Workflow instances', Workflow.objects.count())
        else:
            self.logger.info('Workflow data already exists')
