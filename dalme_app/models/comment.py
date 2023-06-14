import textwrap

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeIntid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Comment(dalmeIntid):
    """Stores comment information."""

    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=55, db_index=True)
    body = models.TextField(blank=True)

    @property
    def snippet(self):
        """Return a snippet of the comment."""
        body_snippet = textwrap.shorten(self.body, width=35, placeholder='...')
        return f'{self.creation_user.username} - {body_snippet}'

    def __str__(self):  # noqa: D105
        return self.snippet

    class Meta:  # noqa: D106
        ordering = ['creation_timestamp']
