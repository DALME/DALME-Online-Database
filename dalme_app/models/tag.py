from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Tag(dalmeUuid):
    """Store tag information."""

    WORKFLOW = 'WF'  # type of tags used to keep track of general DALME workflow
    CONTROL = 'C'  # general purpose control tags
    TICKET = 'T'  # tags for issue ticket management
    TAG_TYPES = (
        (WORKFLOW, 'Workflow'),
        (CONTROL, 'Control'),
        (TICKET, 'Ticket'),
    )
    TICKET_TAGS = (
        ('bug', 'bug'),
        ('feature', 'feature'),
        ('documentation', 'documentation'),
        ('question', 'question'),
        ('content', 'content'),
    )

    tag_type = models.CharField(max_length=2, choices=TAG_TYPES)
    tag = models.CharField(max_length=55, blank=True)
    tag_group = models.CharField(max_length=255, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=55, blank=True, db_index=True)

    class Meta:  # noqa: D106
        unique_together = ('tag', 'object_id')

    def __str__(self):  # noqa: D105
        return self.tag
