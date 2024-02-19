"""Migrate any leftover models and data."""
from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction

from dalme_app.models import Comment, Tag, Task
from ida.models import (
    AttributeType,
    AttributeValueFkey,
    LocaleReference,
    Location,
    Place,
    PublicRegister,
    Relationship,
    RelationshipType,
    Scope,
    ScopeType,
    Tenant,
    User,
)

from .base import BaseStage


class Stage(BaseStage):
    """Data migration for leftover models."""

    name = '09 Finalize'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.migrate_location()
        self.migrate_place()
        self.migrate_credit_support_records()
        self.migrate_record_credits()
        self.migrate_tag()
        self.migrate_comment()
        self.migrate_public_register()
        self.migrate_task()

    @transaction.atomic
    def migrate_location(self):
        """Copy location data.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0010_data_m_basic_types.py#L28

        """
        if Location.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating locale places to locations')
                cursor.execute('SELECT * FROM restore.dalme_app_place WHERE locale_id IS NOT NULL;')
                rows = self.map_rows(cursor)

                locale_at_id = AttributeType.objects.get(name='locale').id
                locale_ct = ContentType.objects.get_for_model(LocaleReference)
                location_ct = ContentType.objects.get_for_model(Location)

                for idx, row in enumerate(rows):  # noqa: B007
                    obj = Location.objects.create(
                        location_type=4,
                        creation_user_id=row['creation_user_id'],
                        modification_user_id=row['modification_user_id'],
                        creation_timestamp=row['creation_timestamp'],
                        modification_timestamp=row['modification_timestamp'],
                    )
                    AttributeValueFkey.objects.create(
                        object_id=obj.id,
                        attribute_type_id=locale_at_id,
                        target_content_type=locale_ct,
                        content_type=location_ct,
                        target_id=row['locale_id'],
                        creation_user_id=row['creation_user_id'],
                        modification_user_id=row['modification_user_id'],
                        creation_timestamp=row['creation_timestamp'],
                        modification_timestamp=row['modification_timestamp'],
                    )

                self.logger.info('Created %s Location instances', idx + 1)
                self.logger.info('Created %s AttributeValueFkey instances', idx + 1)

        else:
            self.logger.info('Location data already exists')

    @transaction.atomic
    def migrate_place(self):
        """Copy place data."""
        if Place.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating places')
                cursor.execute('SELECT * FROM restore.dalme_app_place WHERE locale_id IS NULL;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    row.pop('notes')
                    row.pop('type')
                    row.update({'name': row.pop('standard_name'), 'location_id': row.pop('locale_id')})
                    objs.append(Place(**row))

                Place.objects.bulk_create(objs)
                self.logger.info('Created %s Place instances', Place.objects.count())
        else:
            self.logger.info('Place data already exists')

    @transaction.atomic
    def migrate_credit_support_records(self):
        """Create credit support records.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0008_data_m_misc.py#L94

        """
        if ScopeType.objects.count() == 0:
            self.logger.info('Migrating credit support records')

            user_obj = User.objects.get(pk=1)

            RelationshipType.objects.create(
                name='Authorship',
                short_name='authorship',
                is_directed=True,
                description='The source is, in some capacity, responsible for the creation of the target.',
                creation_user=user_obj,
                modification_user=user_obj,
            )

            ScopeType.objects.create(
                name='Temporal',
                short_name='temporal',
                description='Target is time-constrained within a range (expressed as "start" and "end" parameters) or a duration (as "duration").',
                creation_user=user_obj,
                modification_user=user_obj,
            )

            ScopeType.objects.create(
                name='Spatial',
                short_name='spatial',
                description='Target is spatially-constrained to a geographic location expressed as one of: "polygon" (GIS geometry), "point" (coordinates), or "location" (named, e.g. country, locale, etc.). Point and location can be augmented with an "extents" parameter indicating a ditance from them.',
                creation_user=user_obj,
                modification_user=user_obj,
            )

            ScopeType.objects.create(
                name='Linguistic',
                short_name='linguistic',
                description='Target applies only in the context of a linguistic system, such as a language, dialect, or writing system. Expressed as a reference to a Language Reference record.',
                creation_user=user_obj,
                modification_user=user_obj,
            )

            ctx_scope = ScopeType.objects.create(
                name='Contextual',
                short_name='contextual',
                description='Target is limited to a specific context, broadly defined. A catch-all category designed to help refine the ontology in future.',
                creation_user=user_obj,
                modification_user=user_obj,
            )

            Scope.objects.create(
                scope_type=ctx_scope,
                parameters={'credit': 'editor'},
                notes='Qualifies an authorship relationship, limiting its effects to the receipt of credit in the category indicated by the "credit" parameter. E.g. editor, contributor, corrections.',
                creation_user=user_obj,
                modification_user=user_obj,
            )

            Scope.objects.create(
                scope_type=ctx_scope,
                parameters={'credit': 'contributor'},
                notes='Qualifies an authorship relationship, limiting its effects to the receipt of credit in the category indicated by the "credit" parameter. E.g. editor, contributor, corrections.',
                creation_user=user_obj,
                modification_user=user_obj,
            )

            Scope.objects.create(
                scope_type=ctx_scope,
                parameters={'credit': 'corrections'},
                notes='Qualifies an authorship relationship, limiting its effects to the receipt of credit in the category indicated by the "credit" parameter. E.g. editor, contributor, corrections.',
                creation_user=user_obj,
                modification_user=user_obj,
            )

            self.logger.info("Created '%s' RelationshipType", 'authorship')
            self.logger.info('Created %s ScopeType instances', ScopeType.objects.count())
            self.logger.info('Created %s Scope instances', Scope.objects.count())
        else:
            self.logger.info('Credit support data already exists')

    @transaction.atomic
    def migrate_record_credits(self):  # noqa: PLR0915, C901
        """Migrate records from SourceCredits to relationships.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0008_data_m_misc.py#L175

        """
        if Relationship.objects.count() == 0:
            scope_editor = Scope.objects.get(parameters__credit='editor')
            scope_corrections = Scope.objects.get(parameters__credit='corrections')
            scope_contributor = Scope.objects.get(parameters__credit='contributor')
            authorship = RelationshipType.objects.get(short_name='authorship')
            ct_agent = ContentType.objects.get(app_label='ida', model='agent')
            ct_record = ContentType.objects.get(app_label='ida', model='record')

            with connection.cursor() as cursor:
                self.logger.info('Migrating headwords')
                cursor.execute('SELECT * FROM restore.dalme_app_source_credit;')
                rows = self.map_rows(cursor)

                for row in rows:
                    relationship = Relationship.objects.create(
                        source_content_type=ct_agent,
                        source_object_id=row['agent_id'],
                        target_content_type=ct_record,
                        target_object_id=row['source_id'],
                        rel_type=authorship,
                        notes=row['note'] or 'Stubbed notes field...',
                        creation_user=row['creation_user'],
                        modification_user=row['modification_user'],
                        creation_timestamp=row['creation_timestamp'],
                        modification_timestamp=row['modification_timestamp'],
                    )

                    record_type = row['type']
                    if record_type == 1:
                        relationship.scopes.add(scope_editor)

                    elif record_type == 2:  # noqa: PLR2004
                        relationship.scopes.add(scope_corrections)

                    elif record_type == 3:  # noqa: PLR2004
                        relationship.scopes.add(scope_contributor)

                self.logger.info('Created %s Relationship instances', Relationship.objects.count())
        else:
            self.logger.info('Source credit relationship data already exists')

        @transaction.atomic
        def migrate_tag(self):
            """Copy tag data."""
            # TODO: Some tags have null tag_group field so this fails.
            # dalme=# SELECT DISTINCT tag_group from restore.dalme_app_tag;
            # -[ RECORD 1 ]-----------------------------
            # tag_group |
            # -[ RECORD 2 ]-----------------------------
            # tag_group | DLS_Lucca_Transcription_Review
            # dalme=# SELECT count(*) from restore.dalme_app_tag where tag_group isnull;
            # -[ RECORD 1 ]
            # count | 88
            if Tag.objects.count() == 0:
                with connection.cursor() as cursor:
                    self.logger.info('Migrating tags')
                    tenant_id = Tenant.objects.get(name='DALME').id
                    cursor.execute('SELECT * FROM restore.dalme_app_tag;')
                    rows = self.map_rows(cursor)
                    objs = [
                        Tag(
                            **{
                                **row,
                                'tenant_id': tenant_id,
                                'content_type_id': self.map_content_type(row['content_type_id'], id_only=True),
                            }
                        )
                        for row in rows
                    ]
                    Tag.objects.bulk_create(objs)
                    self.logger.info('Created %s Tag instances', Tag.objects.count())
            else:
                self.logger.info('Tag data already exists')

        @transaction.atomic
        def migrate_comment(self):
            """Copy comment data."""
            if Comment.objects.count() == 0:
                with connection.cursor() as cursor:
                    self.logger.info('Migrating comments')
                    tenant_id = Tenant.objects.get(name='DALME').id
                    cursor.execute('SELECT * FROM restore.dalme_app_comment;')
                    rows = self.map_rows(cursor)
                    objs = [
                        Comment(
                            **{
                                **row,
                                'tenant_id': tenant_id,
                                'content_type_id': self.map_content_type(row['content_type_id'], id_only=True),
                            }
                        )
                        for row in rows
                    ]
                    Comment.objects.bulk_create(objs)
                    self.logger.info('Created %s Comment instances', Comment.objects.count())
            else:
                self.logger.info('Comment data already exists')

        @transaction.atomic
        def migrate_public_register(self):
            """Copy public register data."""
            if PublicRegister.objects.count() == 0:
                with connection.cursor() as cursor:
                    self.logger.info('Migrating public registers')
                    cursor.execute('SELECT * FROM restore.dalme_app_publicregister;')
                    rows = self.map_rows(cursor)
                    objs = [
                        PublicRegister(
                            **{
                                **row,
                                'content_type_id': self.map_content_type(row['content_type_id'], id_only=True),
                            }
                        )
                        for row in rows
                    ]
                    PublicRegister.objects.bulk_create(objs)
                    self.logger.info('Created %s PublicRegister instances', PublicRegister.objects.count())
            else:
                self.logger.info('PublicRegister data already exists')

        @transaction.atomic
        def migrate_task(self):
            """Copy task data.

            https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0008_data_m_misc.py#L44C5-L44C22

            """
            if Task.objects.count() == 0:
                with connection.cursor() as cursor:
                    self.logger.info('Migrating tasks')
                    tenant_id = Tenant.objects.get(name='DALME').id
                    cursor.execute('SELECT * FROM restore.dalme_app_task;')
                    rows = self.map_rows(cursor)

                    for row in rows:
                        row.pop('position')
                        row.pop('created_by_id')
                        assigned_to_id = row.pop('assigned_to_id')
                        workset_id = row.pop('workset_id')
                        file_id = row.pop('file_id')

                        if row['completed']:
                            row.update({'completed_by': row['modification_user_id'], 'tenant_id': tenant_id})

                        obj = Task.objects.create(**row)

                        if assigned_to_id:
                            obj.assignees.add(assigned_to_id)

                        if file_id:
                            obj.files.add(file_id)

                        if workset_id:
                            obj.resources.add(workset_id)

                    self.logger.info('Created %s Task instances', Task.objects.count())
            else:
                self.logger.info('Task data already exists')
