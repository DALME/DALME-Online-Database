"""Migrate dalme_public CMS data."""
from wagtail.models import Page, Revision

from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction

from .base import BaseStage

SOURCE_SCHEMA = 'restore'
CLONED_SCHEMA = 'cloned'


class Stage(BaseStage):
    """Data migration for public/cms models."""

    name = '10 Public/CMS'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.clone_schema()
        self.migrate_schema()
        self.migrate_revision()
        self.drop_schema()

    @transaction.atomic
    def clone_schema(self):
        """Clone the restore schema giving us data we can safely mutate."""
        with connection.cursor() as cursor:
            self.logger.info("Cloning the '%s' schema", SOURCE_SCHEMA)
            cursor.execute('SELECT clone_schema(%s, %s);', [SOURCE_SCHEMA, CLONED_SCHEMA])

    @transaction.atomic
    def migrate_schema(self):
        """Migrate existing CMS tables to the DALME schema."""
        move_cms = """
            DO $$
              DECLARE
              tb text;
            BEGIN
              FOR tb IN
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_name IN
                (SELECT table_name FROM information_schema.tables WHERE table_schema = 'dalme')
                AND table_name <> 'django_admin_log'
                AND table_name <> 'django_content_types'
                AND table_name <> 'django_migrations'
                AND table_name <> 'django_session'
                -- Note, we DO want to move 'django_site' as that's used by Wagtail.
                AND table_name <> 'wagtailcore_revision'
              LOOP
                -- Remove any existing data from the DALME schema per table.
                EXECUTE format('DROP TABLE dalme.%I CASCADE;', tb);

                -- Move the table from the cloned schema to the DALME schema.
                EXECUTE format('ALTER TABLE cloned.%I SET SCHEMA dalme;', tb);
              END LOOP;
            END $$;
        """
        with connection.cursor() as cursor:
            self.logger.info('Migrating CMS data')
            cursor.execute(move_cms)

    @transaction.atomic
    def clone_migrate_revision(self):
        """Migrate pagerevision data to the revision table."""

        def revision_mapper(cursor, page_revision):
            """Remap page revision data to revision data."""
            page_content_type = ContentType.objects.get_for_model(Page)

            page_id = page_revision.pop('page_id')
            content = page_revision.pop('content_json')

            cursor.execute('SELECT * from public.wagtailcore_page WHERE id = %s', [page_id])
            row = cursor.fetchone()
            columns = [col[0] for col in cursor.description]
            data = dict(zip(columns, row))  # noqa: B905

            content_type_id = self.map_content_type(data['content_type_id'], id_only=True)

            return {
                'base_content_type': page_content_type,
                'content_type_id': content_type_id,
                'object_id': page_id,
                'content': content,
                **page_revision,
            }

        with connection.cursor() as cursor:
            self.logger.info('Migrating page revision data')
            cursor.execute('SELECT * from public.wagtailcore_pagerevision;')

            columns = [col[0] for col in cursor.description]
            page_revisions = [dict(zip(columns, row, strict=True)) for row in cursor.fetchall()]
            revisions = [revision_mapper(cursor, page_revision) for page_revision in page_revisions]

            connection.set_schema('dalme', True)
            Revision.objects.bulk_create([Revision(**revision) for revision in revisions], batch_size=1000)

            # TODO: We can now truncate/drop the stale pagerevision table from
            # the 'public' schema.

    @transaction.atomic
    def drop_schema(self):
        """Drop the cloned schema restoring original symmetry."""
        with connection.cursor() as cursor:
            self.logger.info("Dropping the '%s' schema", CLONED_SCHEMA)
            cursor.execute('DROP SCHEMA %s;', [CLONED_SCHEMA])
