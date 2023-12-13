"""Define ORM signals for dalme_app."""
from django_currentuser.middleware import get_current_user

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from .models import (
    Page,
    PublicRegister,
    Record,
    Workflow,
    WorkLog,
    rs_resource,
)


@receiver(models.signals.post_save, sender=Page)
def page_post_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """Run after save method on Page objects."""
    if instance.dam_id is not None:
        rs_image = rs_resource.objects.get(ref=instance.dam_id)
        rs_image.field79 = instance.name
        rs_image.save()


@receiver(models.signals.post_save, sender=Record)
def source_post_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """Run after save method on Record objects."""
    # create workflow record if this is a new source
    if created:
        wf = Workflow(
            source=instance,
            last_modified=timezone.now(),
            last_user=get_current_user(),
        )
        wf.save()
    # create or delete public registration
    public = instance.workflow.is_public
    registration = PublicRegister.objects.filter(object_id=instance.id)
    if public and not registration.exists():
        PublicRegister.objects.create(
            object_id=instance.id,
            content_type=ContentType.objects.get_for_model(instance),
        )
    if not public and registration.exists():
        registration.first().delete()


@receiver(models.signals.pre_delete, sender=Record)
def source_pre_delete(sender, instance, **kwargs):  # noqa: ARG001
    """Run before delete method on Record objects."""
    if instance.pages:
        for page in instance.pages.all():
            if page.records:
                for sp in page.records.all():
                    if sp.transcription:
                        sp.transcription.delete()
            page.delete()

    pr = PublicRegister.objects.filter(object_id=instance.id)
    if pr.exists():
        pr.first().delete()


@receiver(models.signals.post_save, sender=Workflow)
def workflow_post_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """Run after save method on Workflow objects."""
    if not created:
        models.signals.post_save.send(sender=Record, instance=instance.source, created=False)
    else:
        WorkLog.objects.update_or_create(source=instance, event='Record created', timestamp=instance.last_modified)
