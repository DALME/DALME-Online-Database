"""Define ORM signals for dalme_app."""
from django.db import models
from django.dispatch import receiver

from ida.models import Record

from .models import Workflow, WorkLog


@receiver(models.signals.post_save, sender=Workflow)
def workflow_post_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """Run after save method on Workflow objects."""
    if not created:
        models.signals.post_save.send(sender=Record, instance=instance.source, created=False)
    else:
        WorkLog.objects.update_or_create(source=instance, event='Record created', timestamp=instance.last_modified)
