from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from django_currentuser.middleware import get_current_user
from dalme_app.models import rs_resource, Workflow, Work_log, Page, PublicRegister, Set_x_content, Source, Transcription, Source_pages
from django.contrib.contenttypes.models import ContentType


@receiver(models.signals.post_save, sender=Page)
def page_post_save(sender, instance, created, **kwargs):
    if instance.dam_id is not None:
        rs_image = rs_resource.objects.get(ref=instance.dam_id)
        rs_image.field79 = instance.name
        rs_image.save()


@receiver(models.signals.post_save, sender=Source)
def source_post_save(sender, instance, created, **kwargs):
    # create workflow record if this is a new source
    if created and instance.type == 13:
        wf = Workflow(
         source=instance,
         last_modified=timezone.now(),
         last_user=get_current_user()
        )
        wf.save()

    if instance.type == 13:
        # update dataset
        if instance.primary_dataset is not None:
            Set_x_content.objects.update_or_create(
                set_id=instance.primary_dataset,
                object_id=instance.id,
                content_type=ContentType.objects.get_for_model(instance)
            )
        # create or delete public registration
        public = instance.workflow.is_public
        registration = PublicRegister.objects.filter(object_id=instance.id)
        if public and not registration.exists():
            PublicRegister.objects.create(
                object_id=instance.id,
                content_type=ContentType.objects.get_for_model(instance)
            )
        if not public and registration.exists():
            registration.first().delete()


@receiver(models.signals.pre_delete, sender=Source)
def source_pre_delete(sender, instance, **kwargs):
    if instance.pages:
        for page in instance.pages.all():
            if page.sources:
                for sp in page.sources.all():
                    if sp.transcription:
                        sp.transcription.delete()
            page.delete()

    pr = PublicRegister.objects.filter(object_id=instance.id)
    if pr.exists():
        pr.first().delete()


@receiver(models.signals.post_save, sender=Transcription)
def transcription_post_save(sender, instance, created, **kwargs):
    source_pages = instance.source_pages.all()
    if source_pages.exists():
        for sp in source_pages:
            source = sp.source
            # update source tracking
            source.modification_timestamp = timezone.now()
            source.modification_user = get_current_user()
            source.save()
            # emit post_save signal on source_page for indexing
            models.signals.post_save.send(sender=Source_pages, instance=sp, created=False)


@receiver(models.signals.post_save, sender=Workflow)
def workflow_post_save(sender, instance, created, **kwargs):
    if not created:
        models.signals.post_save.send(sender=Source, instance=instance.source, created=False)
    else:
        Work_log.objects.update_or_create(source=instance, event='Source created', timestamp=instance.last_modified)
