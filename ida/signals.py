"""Define ORM signals for the ida."""
from django_currentuser.middleware import get_current_user

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from dalme_app.models import Workflow

from .models import Folio, Page, PublicRegister, Record, Transcription, rs_resource


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
    # Create workflow record if this is a new source.
    if created:
        wf = Workflow(
            source=instance,
            last_modified=timezone.now(),
            last_user=get_current_user(),
        )
        wf.save()

    # Create or delete public registration.
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


@receiver(models.signals.post_save, sender=Transcription)
def transcription_post_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """Run after save method on Transcription objects."""
    if instance.folios.exists():
        for folio in instance.folios.all():
            source = folio.source

            # Update source tracking.
            source.modification_timestamp = timezone.now()
            source.modification_user = get_current_user()
            source.save()

            # Emit the post_save signal on source_page for indexing purposes.
            models.signals.post_save.send(sender=Folio, instance=folio, created=False)
