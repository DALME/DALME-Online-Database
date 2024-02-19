"""Migrate rank 2 (two dependencies other than auth) models."""
from django.db import connection, transaction

from ida.models import ObjectAttribute, Token

from .base import BaseStage


class Stage(BaseStage):
    """Data migration for rank 2 models."""

    name = '04 Rank Two'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.migrate_object_attribute()
        self.migrate_token()

    @transaction.atomic
    def migrate_object_attribute(self):
        """Copy object attribute data."""
        if ObjectAttribute.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating object attributes')
                cursor.execute('SELECT * FROM restore.dalme_app_object;')
                rows = self.map_rows(cursor)
                objs = [ObjectAttribute(**row) for row in rows]
                ObjectAttribute.objects.bulk_create(objs)
                self.logger.info('Created %s ObjectAttribute instances', ObjectAttribute.objects.count())
        else:
            self.logger.info('ObjectAttribute data already exists')

    @transaction.atomic
    def migrate_token(self):
        """Copy token data."""
        if Token.objects.count() == 0:
            with connection.cursor() as cursor:
                self.logger.info('Migrating tokens')
                cursor.execute('SELECT * FROM restore.dalme_app_token;')
                rows = self.map_rows(cursor)

                objs = []
                for row in rows:
                    object_phrase_id = row.pop('object_phrase_id_id')
                    wordform_id = row.pop('wordform_phrase_id_id')
                    row.update({'object_phrase_id': object_phrase_id, 'wordform_id': wordform_id})
                    objs.append(Token(**row))

                Token.objects.bulk_create(objs)
                self.logger.info('Created %s Token instances', Token.objects.count())
        else:
            self.logger.info('Token data already exists')
