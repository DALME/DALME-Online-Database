"""Migrate public CMS data."""

from django_tenants.utils import schema_context

from django.contrib.contenttypes.models import ContentType
from django.db import connection, transaction

from ida.models import Profile, User

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
        self.drop_cloned_schema()
        self.fix_contentypes()
        self.transfer_avatars()
        self.transfer_snippets()
        self.drop_restore_schema()

    @transaction.atomic
    def clone_schema(self):
        """Clone the restore schema giving us data we can safely mutate."""
        with connection.cursor() as cursor:
            self.logger.info("Cloning the '%s' schema", SOURCE_SCHEMA)
            cursor.execute("SELECT clone_schema(%s, %s, 'DATA');", [SOURCE_SCHEMA, CLONED_SCHEMA])

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
                WHERE table_schema = 'cloned'
                AND table_name IN
                (SELECT table_name FROM information_schema.tables WHERE table_schema = 'dalme')
                AND table_name <> 'django_admin_log'
                AND table_name <> 'django_content_types'
                AND table_name <> 'django_migrations'
                AND table_name <> 'django_session'
                AND table_name <> 'public_recordbrowser'
                AND table_name <> 'public_recordviewer'
                AND table_name <> 'public_footer'
                AND table_name <> 'public_searchpage'
                AND table_name <> 'public_explorepage'
                -- Note, we DO want to move 'django_site' as that's used by Wagtail.
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
    def drop_cloned_schema(self):
        """Drop the cloned schema restoring original symmetry."""
        with connection.cursor() as cursor:
            self.logger.info("Dropping the '%s' schema", CLONED_SCHEMA)
            cursor.execute('DROP SCHEMA cloned CASCADE')

    @transaction.atomic
    def fix_contentypes(self):
        """Replace references to contentypes with new values."""
        with schema_context('dalme'):
            self.logger.info('Replacing stale content type references')
            from wagtail.models import Page, PageLogEntry, Revision, Task, TaskState, WorkflowState

            page_type = ContentType.objects.get(app_label='wagtailcore', model='page')

            # fix page revisions
            self.logger.info('Processing page revisions')
            for rev in Revision.objects.all():
                new_ct = self.map_content_type(rev.content_type_id, id_only=True)
                rev.content_type_id = new_ct
                rev.base_content_type_id = page_type
                rev.content['content_type'] = new_ct
                rev.save(update_fields=['content_type_id', 'base_content_type_id', 'content'])

            # fix pages
            self.logger.info('Processing pages')
            for page in Page.objects.all():
                new_ct = self.map_content_type(page.content_type_id, id_only=True)
                page.content_type_id = new_ct
                page.save(update_fields=['content_type_id'])

            # fix page log entries
            self.logger.info('Processing page logs')
            for entry in PageLogEntry.objects.all():
                # there are constraints for page_id and user_id, so that if either has been deleted
                # save() will fail validation, so we need to check before trying to update
                if Page.objects.filter(pk=entry.page_id).exists() and User.objects.filter(pk=entry.user_id).exists():
                    new_ct = self.map_content_type(entry.content_type_id, id_only=True)
                    entry.content_type_id = new_ct
                    entry.save(update_fields=['content_type_id'])
                else:
                    entry.delete()

            # fix tasks
            self.logger.info('Processing tasks')
            for task in Task.objects.all():
                new_ct = self.map_content_type(task.content_type_id, id_only=True)
                task.content_type_id = new_ct
                task.save(update_fields=['content_type_id'])

            # fix task states
            self.logger.info('Processing task states')
            for ts in TaskState.objects.all():
                new_ct = self.map_content_type(ts.content_type_id, id_only=True)
                ts.content_type_id = new_ct
                ts.save(update_fields=['content_type_id'])

            # fix workflow states
            self.logger.info('Processing workflow states')
            for ws in WorkflowState.objects.all():
                new_ct = self.map_content_type(ws.content_type_id, id_only=True)
                new_base_ct = self.map_content_type(ws.base_content_type_id, id_only=True)
                ws.content_type_id = new_ct
                ws.base_content_type_id = new_base_ct
                ws.save(update_fields=['content_type_id', 'base_content_type_id'])

    @transaction.atomic
    def transfer_avatars(self):
        """Transfer avatar field from wagtail to profile."""
        with connection.cursor() as cursor:
            self.logger.info('Transfering avatars')
            cursor.execute('SELECT * FROM restore.wagtailusers_userprofile;')
            rows = self.map_rows(cursor)
            for row in rows:
                if row['avatar']:
                    profile = Profile.objects.get(user=row['user_id'])
                    profile.avatar = row['avatar']
                    profile.save(update_fields=['avatar'])

    @transaction.atomic
    def transfer_snippets(self):
        """Transfer snippet data to settings table."""
        data = {}

        with connection.cursor() as cursor:
            self.logger.info('Transfering snippet data')
            # footer
            cursor.execute('SELECT * FROM restore.public_footer;')
            row = next(self.map_rows(cursor))
            data.update(
                {
                    'footer_links': row['pages'],
                    'footer_social': row['social'],
                }
            )
            # searchpage
            cursor.execute('SELECT * FROM restore.public_searchpage;')
            row = next(self.map_rows(cursor))
            data.update(
                {
                    'search_help_content': row['help_content'],
                    'search_header_image': row['header_image_id'],
                    'search_header_position': row['header_position'],
                }
            )
            # explorepage
            cursor.execute('SELECT * FROM restore.public_explorepage;')
            row = next(self.map_rows(cursor))
            data.update(
                {
                    'explore_text_before': row['text_before'],
                    'explore_text_after': row['text_after'],
                    'explore_header_image': row['header_image_id'],
                    'explore_header_position': row['header_position'],
                }
            )
            # recordbrowser
            cursor.execute('SELECT * FROM restore.public_recordbrowser;')
            row = next(self.map_rows(cursor))
            data.update(
                {
                    'browser_header_image': row['header_image_id'],
                    'browser_header_position': row['header_position'],
                }
            )
            # recordviewer
            cursor.execute('SELECT * FROM restore.public_recordviewer;')
            row = next(self.map_rows(cursor))
            data.update(
                {
                    'viewer_header_image': row['header_image_id'],
                    'viewer_header_position': row['header_position'],
                }
            )

            with schema_context('dalme'):
                from public.models import BaseImage, Settings

                data.update(
                    {
                        'search_header_image': BaseImage.objects.get(pk=data['search_header_image']),
                        'explore_header_image': BaseImage.objects.get(pk=data['explore_header_image']),
                        'browser_header_image': BaseImage.objects.get(pk=data['browser_header_image']),
                        'viewer_header_image': BaseImage.objects.get(pk=data['viewer_header_image']),
                    }
                )

                Settings.objects.create(
                    name='DALME',
                    tagline='The Documentary Archaeology of Late Medieval Europe',
                    logo='images/dalme_logo.svg',
                    copyright_line='The Documentary Archaeology of Late Medieval Europe',
                    **data,
                )

    @transaction.atomic
    def drop_restore_schema(self):
        """Drop the restore schema."""
        with connection.cursor() as cursor:
            self.logger.info("Dropping the '%s' schema", SOURCE_SCHEMA)
            cursor.execute('DROP SCHEMA restore CASCADE')
