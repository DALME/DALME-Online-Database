"""Define ORM signals for the ida."""
from django_currentuser.middleware import get_current_user

from django.db import models
from django.dispatch import receiver
from django.utils import timezone

from .models import Folio, Page, Transcription, rs_resource


@receiver(models.signals.post_save, sender=Page)
def page_post_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """Run after save method on Page objects."""
    if instance.dam_id is not None:
        rs_image = rs_resource.objects.get(ref=instance.dam_id)
        rs_image.field79 = instance.name
        rs_image.save()


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
