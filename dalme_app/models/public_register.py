from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options
from django_currentuser.middleware import get_current_user

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ("in_db",)


class PublicRegister(models.Model):
    """
    OBSOLETE: no longer read or maintained.

    This table used to back the purl endpoint and was kept in sync by
    `source_post_save`/`source_pre_delete` in dalme_app/signals.py. It drifted
    out of sync with `Workflow.is_public`, so the purl endpoint now queries
    `Source.objects.filter(workflow__is_public=True)` directly and the sync
    signals have been removed. The model and table are kept for now only as
    a fallback, its contents are stale and should not be relied upon.
    """

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField(db_index=True, primary_key=True)
    content_object = GenericForeignKey("content_type", "object_id")
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        default=get_current_user,
        related_name="%(app_label)s_%(class)s_creation",
        null=True,
    )
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
