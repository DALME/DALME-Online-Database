"""Migrate rank 1 (one dependency other than auth) models."""

from django.db import connection, transaction

from ida.models import (
    EntityPhrase,
    Headword,
    LocaleReference,
    Object,
    RightsPolicy,
    Scope,
    Ticket,
    Wordform,
)

from .base import BaseStage


class Stage(BaseStage):
    """Data migration for rank 1 models."""

    name = '03 Rank One'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.migrate_headword()
        self.migrate_object()
        self.migrate_rights_policy()
        self.migrate_scope()
        self.migrate_locale_reference()
        self.migrate_wordform()
        self.migrate_entity_phrase()
        self.migrate_ticket()

    @transaction.atomic
    def migrate_headword(self):
        """Copy headword data."""
        if Headword.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating headwords')
                cursor.execute('SELECT * FROM restore.core_headword;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    concept_id = row.pop('concept_id_id')
                    row.update({'concept_id': concept_id})
                    objs.append(Headword(**row))

                Headword.objects.bulk_create(objs)
                self.logger.info('Created %s Headword instances', Headword.objects.count())
        else:
            self.logger.info('Headword data already exists')

    @transaction.atomic
    def migrate_object(self):
        """Copy object data."""
        if Object.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating objects')
                cursor.execute('SELECT * FROM restore.core_object;')
                rows = self.map_rows(cursor)
                objs = [Object(**row) for row in rows]
                Object.objects.bulk_create(objs)
                self.logger.info('Created %s Object instances', Object.objects.count())
        else:
            self.logger.info('Object data already exists')

    @transaction.atomic
    def migrate_rights_policy(self):
        """Copy rights policy data."""
        if RightsPolicy.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating rights policies')
                cursor.execute('SELECT * FROM restore.core_rightspolicy;')
                rows = self.map_rows(cursor)
                objs = [RightsPolicy(**row) for row in rows]
                RightsPolicy.objects.bulk_create(objs)
                self.logger.info('Created %s RightsPolicy instances', RightsPolicy.objects.count())
        else:
            self.logger.info('RightsPolicy data already exists')

    @transaction.atomic
    def migrate_scope(self):
        """Copy scope data."""
        if Scope.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating scopes')
                cursor.execute('SELECT * FROM restore.core_scope;')
                rows = self.map_rows(cursor)
                objs = [Scope(**row) for row in rows]
                Scope.objects.bulk_create(objs)
                self.logger.info('Created %s Scope instances', Scope.objects.count())
        else:
            self.logger.info('Scope data already exists')

    @transaction.atomic
    def migrate_locale_reference(self):
        """Copy locale reference data."""
        if LocaleReference.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating locale references')
                cursor.execute('SELECT * FROM restore.core_localereference;')
                rows = self.map_rows(cursor)
                objs = [LocaleReference(**row) for row in rows]
                LocaleReference.objects.bulk_create(objs)
                self.logger.info('Created %s LocaleReference instances', LocaleReference.objects.count())
        else:
            self.logger.info('LocaleReference data already exists')

    @transaction.atomic
    def migrate_wordform(self):
        """Copy wordform data."""
        if Wordform.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating wordforms')
                cursor.execute('SELECT * FROM restore.core_wordform;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    headword_id = row.pop('headword_id_id')
                    row.update({'headword_id': headword_id})
                    objs.append(Wordform(**row))

                Wordform.objects.bulk_create(objs)
                self.logger.info('Created %s Wordform instances', Wordform.objects.count())
        else:
            self.logger.info('Wordform data already exists')

    @transaction.atomic
    def migrate_entity_phrase(self):
        """Copy entity phrase data.

        This has a generic foreign key but the only content types it points to
        are 'agent' and 'place' so we are ok to key the rows at this point.

        dalme=# select distinct ct.id, ct.model from restore.core_entity_phrase e inner join restore.django_content_type ct on e.content_type_id = ct.id;
        -[ RECORD 1 ]
        id    | 115
        model | place
        -[ RECORD 2 ]
        id    | 104
        model | agent

        """
        if EntityPhrase.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating entity phrases')
                cursor.execute('SELECT * FROM restore.core_entity_phrase;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    transcription_id = row.pop('transcription_id_id')
                    row.update(
                        {
                            'transcription_id': transcription_id,
                            'content_type_id': self.map_content_type(row['content_type_id'], id_only=True),
                        }
                    )
                    objs.append(EntityPhrase(**row))

                EntityPhrase.objects.bulk_create(objs)
                self.logger.info('Created %s EntityPhrase instances', EntityPhrase.objects.count())
        else:
            self.logger.info('EntityPhrase data already exists')

    @transaction.atomic
    def migrate_ticket(self):
        """Copy ticket data.

        https://github.com/ocp/DALME-Online-Database/blob/bc4ff5979e14d14c8cd8a9a9d2f1052512c5388d/core/migrations/0008_data_m_misc.py#L67

        """
        if Ticket.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating tickets')
                cursor.execute('SELECT * FROM restore.core_ticket;')
                rows = self.map_rows(cursor)

                for row in rows:
                    file_id = row.pop('file_id')
                    # We need to populate the m2m field so we can't use bulk
                    # create here but it's only 87 records so not to worry.
                    ticket = Ticket.objects.create(**row)
                    if file_id:
                        ticket.files.add(file_id)

                self.logger.info('Created %s Ticket instances', Ticket.objects.count())
        else:
            self.logger.info('Ticket data already exists')
