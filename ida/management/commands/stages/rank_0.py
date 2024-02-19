"""Migrate rank 0 (no dependencies other than auth) models."""
from django.db import connection, transaction

from dalme_app.models import Attachment, SavedSearch, TaskList
from ida.models import (
    Agent,
    AttributeReference,
    Concept,
    CountryReference,
    LanguageReference,
    Page,
    Person,
    Tenant,
    Transcription,
)

from .base import BaseStage


class Stage(BaseStage):
    """Data migration for rank 0 models."""

    name = '02 Rank Zero'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.migrate_pages()
        self.migrate_concept()
        self.migrate_transcription()
        self.migrate_agent()
        self.migrate_person()
        self.migrate_attachment()
        self.migrate_saved_search()
        self.migrate_tasklist()
        self.migrate_attribute_reference()
        self.migrate_country_reference()
        self.migrate_language_reference()

    # IDA models.
    @transaction.atomic
    def migrate_pages(self):
        """Copy page data."""
        # TODO: All page.canvas data is null so this fails.
        if Page.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating pages')
                cursor.execute('SELECT * FROM restore.dalme_app_page;')
                rows = self.map_rows(cursor)
                objs = [Page(**row) for row in rows]
                Page.objects.bulk_create(objs)
                self.logger.info('Created %s Page instances', Page.objects.count())
        else:
            self.logger.info('Page data already exists')

    @transaction.atomic
    def migrate_concept(self):
        """Copy concept data."""
        if Concept.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating concepts')
                cursor.execute('SELECT * FROM restore.dalme_app_concept;')
                rows = self.map_rows(cursor)
                objs = [Concept(**row) for row in rows]
                Concept.objects.bulk_create(objs)
                self.logger.info('Created %s Concept instances', Concept.objects.count())
        else:
            self.logger.info('Concept data already exists')

    @transaction.atomic
    def migrate_transcription(self):
        """Copy transcription data."""
        # NOTE: Some transcription.version data is null. In those cases, I've
        # assumed it's just 1 as the model field default suggests.
        if Transcription.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating transcriptions')
                cursor.execute('SELECT * FROM restore.dalme_app_transcription;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    if row['version'] is None:
                        row.update({'version': 1})
                    objs.append(Transcription(**row))

                Transcription.objects.bulk_create(objs)
                self.logger.info('Created %s Transcription instances', Transcription.objects.count())
        else:
            self.logger.info('Transcription data already exists')

    @transaction.atomic
    def migrate_agent(self):
        """Copy agent data."""
        if Agent.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating agents')
                cursor.execute('SELECT * FROM restore.dalme_app_agent ORDER BY creation_timestamp;')
                rows = self.map_rows(cursor)

                seen = set()
                objs = []
                for row in rows:
                    user_id = row.pop('user_id')
                    if user_id in seen:
                        self.logger.info('Skipping Agent duplicate for user_id: %s', user_id)
                        continue

                    if user_id is not None:
                        seen.add(user_id)

                    row.pop('notes')
                    row.update({'agent_type': row.pop('type'), 'name': row.pop('standard_name')})
                    objs.append(Agent(**row))

                self.logger.info('Created %s Agent instances', Agent.objects.count())
        else:
            self.logger.info('Agent data already exists')

    @transaction.atomic
    def migrate_person(self):
        """Split person records out of existing agents.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0010_data_m_basic_types.py#L5

        """
        if Person.objects.count() == 0:
            self.logger.info('Migrating people')
            with connection.cursor() as cursor:
                self.logger.info('Migrating people (from agents)')
                cursor.execute('SELECT * FROM restore.dalme_app_agent WHERE type = 1 ORDER BY creation_timestamp;')
                rows = self.map_rows(cursor)

                seen = set()
                for row in rows:
                    user_id = row['user_id']
                    if user_id in seen:
                        self.logger.info('Skipping Person duplicate with user_id: %s', user_id)
                        continue

                    if user_id is not None:
                        seen.add(user_id)

                    row.pop('id')
                    row.pop('notes')
                    row.update({'agent_type': row.pop('type'), 'name': row.pop('standard_name')})
                    # Note, we can't bulk create a multitable-inherited model
                    # so here we'll just save each one individually.
                    Person.objects.create(**row)

                self.logger.info('Created %s Person instances', Person.objects.count())
        else:
            self.logger.info('Person data already exists')

    # These dalme_app models also need to be scoped to the DALME tenant so we
    # can do that as we proceed.
    @transaction.atomic
    def migrate_attachment(self):
        """Copy attachment data."""
        if Attachment.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating attachments')
                tenant_id = Tenant.objects.get(name='DALME').id
                cursor.execute('SELECT * FROM restore.dalme_app_attachment;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    filefield = row.pop('file')
                    filetype = row.pop('type')
                    objs.append(
                        Attachment(**{**row, 'tenant_id': tenant_id, 'filefield': filefield, 'filetype': filetype})
                    )

                Attachment.objects.bulk_create(objs)
                self.logger.info('Created %s Attachment instances', Attachment.objects.count())
        else:
            self.logger.info('Attachment data already exists')

    @transaction.atomic
    def migrate_saved_search(self):
        """Copy saved search data."""
        if SavedSearch.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating saved searches')
                tenant_id = Tenant.objects.get(name='DALME').id
                cursor.execute('SELECT * FROM restore.dalme_app_savedsearch;')
                rows = self.map_rows(cursor)
                objs = [SavedSearch(**{**row, 'tenant_id': tenant_id}) for row in rows]
                SavedSearch.objects.bulk_create(objs)
                self.logger.info('Created %s SavedSearch instances', SavedSearch.objects.count())
        else:
            self.logger.info('SavedSearch data already exists')

    @transaction.atomic
    def migrate_tasklist(self):
        """Copy task list data."""
        if TaskList.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating task lists')
                tenant_id = Tenant.objects.get(name='DALME').id
                cursor.execute('SELECT * FROM restore.dalme_app_tasklist;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    team_link_id = row.pop('group_id')
                    objs.append(TaskList(**{**row, 'tenant_id': tenant_id, 'team_link_id': team_link_id}))

                TaskList.objects.bulk_create(objs)
                self.logger.info('Created %s TaskList instances', TaskList.objects.count())
        else:
            self.logger.info('TaskList data already exists')

    @transaction.atomic
    def migrate_attribute_reference(self):
        """Copy attribute reference data."""
        if AttributeReference.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating attribute references')
                cursor.execute('SELECT * FROM restore.dalme_app_attributereference;')
                rows = self.map_rows(cursor)
                objs = [AttributeReference(**row) for row in rows]
                AttributeReference.objects.bulk_create(objs)
                self.logger.info('Created %s AttributeReference instances', AttributeReference.objects.count())
        else:
            self.logger.info('AttributeReference data already exists')

    @transaction.atomic
    def migrate_country_reference(self):
        """Copy country reference data."""
        if CountryReference.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating country references')
                cursor.execute('SELECT * FROM restore.dalme_app_countryreference;')
                rows = self.map_rows(cursor)
                objs = [CountryReference(**row) for row in rows]
                CountryReference.objects.bulk_create(objs)
                self.logger.info('Created %s CountryReference instances', CountryReference.objects.count())
        else:
            self.logger.info('CountryReference data already exists')

    @transaction.atomic
    def migrate_language_reference(self):
        """Copy language reference data.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/dalme_app/migrations/0010_data_m_basic_types.py#L5

        """
        if LanguageReference.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating language references')
                cursor.execute('SELECT * FROM restore.dalme_app_languagereference;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    dialect_type = 2
                    lang_type = row.pop('type')
                    row['is_dialect'] = lang_type == dialect_type
                    objs.append(LanguageReference(**row))

                LanguageReference.objects.bulk_create(objs)
                self.logger.info('Created %s LanguageReference instances', LanguageReference.objects.count())
        else:
            self.logger.info('LanguageReference data already exists')
