from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
import textwrap
from dalme_app.models._templates import dalmeIntid
import django.db.models.options as options


options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Comment(dalmeIntid):
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=55, null=True, db_index=True)
    body = models.TextField(blank=True, null=True, default=None)

    @property
    def snippet(self):
        body_snippet = textwrap.shorten(self.body, width=35, placeholder="...")
        return "{author} - {snippet}...".format(author=self.creation_user.username, snippet=body_snippet)

    def __str__(self):
        return self.snippet

    class Meta:
        ordering = ['creation_timestamp']
