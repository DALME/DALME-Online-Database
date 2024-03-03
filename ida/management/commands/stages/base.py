"""Base class for a data migration stage."""

import abc
import functools

import structlog

from django.contrib.contenttypes.models import ContentType
from django.db import connection

logger = structlog.get_logger(__name__)

# Here are some useful statements if you want to compare ContentType diffs.
# SELECT * FROM public.django_content_type new_ct INNER JOIN restore.django_content_type old_ct ON new_ct.model = old_ct.model;
# SELECT * FROM public.django_content_type new_ct INNER JOIN restore.django_content_type old_ct ON new_ct.model = old_ct.model
# WHERE new_ct.app_label != old_ct.app_label;
ALTERED_MODEL_MAP = {
    ('core', 'agent'): 'ida.agent',
    ('core', 'attribute_type'): 'ida.attributetype',
    ('core', 'concept'): 'ida.concept',
    ('core', 'content_type'): 'ida.contenttypeextended',
    ('core', 'countryreference'): 'ida.countryreference',
    ('core', 'entity_phrase'): 'ida.entityphrase',
    ('core', 'headword'): 'ida.headword',
    ('core', 'object'): 'ida.object',
    ('core', 'object_attribute'): 'ida.objectattribute',
    ('core', 'page'): 'ida.page',
    ('core', 'place'): 'ida.place',
    ('core', 'set'): 'ida.collection',
    ('core', 'set_x_content'): 'ida.collectionmembership',
    ('core', 'source'): 'ida.record',
    ('core', 'source_credit'): 'ida.relationship',
    ('core', 'source_pages'): 'ida.pagenode',
    ('core', 'ticket'): 'ida.ticket',
    ('core', 'token'): 'ida.token',
    ('core', 'transcription'): 'ida.transcription',
    ('core', 'wordform'): 'ida.wordform',
    ('core', 'work_log'): 'ida.worklog',
    ('core', 'work_flow'): 'ida.workflow',
    ('core', 'task'): 'ida.task',
    ('core', 'tasklist'): 'ida.tasklist',
    ('core', 'comment'): 'ida.comment',
    ('core', 'collection'): 'ida.collection',
    ('core', 'collectionmembership'): 'ida.collectionmembership',
    ('core', 'attachment'): 'ida.attachment',
    ('core', 'savedsearch'): 'ida.savedsearch',
    ('core', 'tag'): 'ida.tag',
}

SOURCES_MODEL_MAP = {
    1: ('ida', 'publication'),
    2: ('ida', 'publication'),
    3: ('ida', 'publication'),
    4: ('ida', 'publication'),
    5: ('ida', 'publication'),
    6: ('ida', 'publication'),
    7: ('ida', 'publication'),
    8: ('ida', 'publication'),
    9: ('ida', 'publication'),
    10: ('ida', 'publication'),
    11: ('ida', 'publication'),
    12: ('ida', 'recordgroup'),
    19: ('ida', 'organization'),
}


class MigrationError(Exception):
    """Raise this exception anywhere within a stage to abort the transaction."""


class BaseStage(abc.ABC):
    """Interface for a data migration stage."""

    @abc.abstractmethod
    def apply(self):
        """Execute the migration stage."""
        ...

    @property
    def logger(self):
        """Provide the logger to all inheriting classes."""
        return logger

    @functools.cached_property
    def old_content_types_index(self):
        """Index the content types from the data being migrated."""
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM restore.django_content_type')
            rows = self.map_rows(cursor)

            index = {}
            for ct in rows:
                if (ct['app_label'], ct['model']) in ALTERED_MODEL_MAP:
                    # Let's just update these on the fly to the new values and
                    # it reduces the overall complexity of the transformation.
                    app_label, model = ALTERED_MODEL_MAP[('core', ct['model'])].split('.')
                else:
                    app_label, model = (ct['app_label'], ct['model'])

                ct_id = ct['id']
                # Return the data as the key into the new_cts index.
                index[ct_id] = (app_label, model)

            return index

    @functools.cached_property
    def new_content_types_index(self):
        """Index the content types from the current db state."""
        index = {}
        for ct in ContentType.objects.all():
            app_label = ct.app_label
            model = ct.model
            key = (app_label, model)
            index[key] = {'id': ct.id, 'model': model, 'app_label': app_label}

        return index

    @staticmethod
    def map_rows(cursor):
        """Map db rows from tuples to dictionaries."""
        columns = [col[0] for col in cursor.description]
        return (dict(zip(columns, row, strict=True)) for row in cursor.fetchall())

    def map_content_type(self, old_id, id_only=False):
        """Map an old content type to a new content type."""
        if not old_id:
            return None
        if id_only and old_id in SOURCES_MODEL_MAP:
            key = SOURCES_MODEL_MAP[old_id]
            return self.new_content_types_index[key]['id']
        key = self.old_content_types_index[old_id]
        if id_only:
            return self.new_content_types_index[key]['id']
        return self.new_content_types_index[key]
