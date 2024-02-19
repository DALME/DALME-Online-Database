"""Base class for a data migration stage."""
import abc
import functools

import structlog

from django.contrib.contenttypes.models import ContentType
from django.db import connection

logger = structlog.get_logger(__name__)

# Here are some useful statements if you want to compare ContentType diffs.
# SELECT * FROM public.django_content_type new_ct INNER JOIN restore.django_content_type old_ct ON new_ct.model = old_ct.model;
# SELECT * FROM public.django_content_type new_ct INNER JOIN restore.django_content_type old_ct ON new_ct.model = old_ct.model WHERE new_ct.app_label != old_ct.app_label;
ALTERED_MODEL_MAP = {
    ('dalme_app', 'agent'): 'ida.agent',
    ('dalme_app', 'attribute_type'): 'ida.attributetype',
    ('dalme_app', 'concept'): 'ida.concept',
    ('dalme_app', 'content_type'): 'ida.contenttypeextended',
    ('dalme_app', 'countryreference'): 'ida.countryreference',
    ('dalme_app', 'entity_phrase'): 'ida.entityphrase',
    ('dalme_app', 'headword'): 'ida.headword',
    ('dalme_app', 'object'): 'ida.object',
    ('dalme_app', 'object_attribute'): 'ida.objectattribute',
    ('dalme_app', 'page'): 'ida.page',
    ('dalme_app', 'place'): 'ida.place',
    ('dalme_app', 'set'): 'dalme_app.collection',
    ('dalme_app', 'set_x_content'): 'dalme_app.collectionmembership',
    ('dalme_app', 'source'): 'ida.record',
    ('dalme_app', 'source_credit'): 'ida.relationship',
    ('dalme_app', 'source_pages'): 'ida.folio',
    ('dalme_app', 'ticket'): 'ida.ticket',
    ('dalme_app', 'token'): 'ida.token',
    ('dalme_app', 'transcription'): 'ida.transcription',
    ('dalme_app', 'wordform'): 'ida.wordform',
    ('dalme_app', 'work_log'): 'dalme_app.worklog',
    ('dalme_app', 'work_flow'): 'dalme_app.workflow',
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
                    app_label, model = ALTERED_MODEL_MAP[('dalme_app', ct['model'])].split('.')
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
        key = self.old_content_types_index[old_id]
        if id_only:
            return self.new_content_types_index[key]['id']
        return self.new_content_types_index[key]
