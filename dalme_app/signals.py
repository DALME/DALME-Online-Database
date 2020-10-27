from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from dalme_app.models._templates import get_current_user
from dalme_app.models import rs_resource, Workflow, Work_log, Page, Set_x_content, Source, Transcription
from django.contrib.contenttypes.models import ContentType


@receiver(models.signals.post_save, sender=Page)
def update_folio(sender, instance, created, **kwargs):
    if instance.dam_id is not None:
        rs_image = rs_resource.objects.get(ref=instance.dam_id)
        rs_image.field79 = instance.name
        rs_image.save()


@receiver(models.signals.post_save, sender=Source)
def update_workflow(sender, instance, created, **kwargs):
    if instance.has_inventory:
        if created:
            wf_object = Workflow.objects.create(source=instance, last_modified=instance.modification_timestamp)
            Work_log.objects.create(source=wf_object, event='Source created', timestamp=wf_object.last_modified)
        else:
            wf_object = Workflow.objects.get_or_create(source=instance, defaults={
                'last_modified': timezone.now(),
                'last_user': get_current_user()
            })
            if type(wf_object) is tuple:
                wf_object[0].last_modified = timezone.now()
                wf_object[0].last_user = get_current_user()
                wf_object[0].save()


@receiver(models.signals.post_save, sender=Source)
def update_dataset(sender, instance, created, **kwargs):
    if instance.type == 13 and instance.primary_dataset is not None:
        if not Set_x_content.objects.filter(set_id=instance.primary_dataset, object_id=instance.id).exists():
            ct = ContentType.objects.get(pk=125)
            Set_x_content.objects.create(set_id=instance.primary_dataset, object_id=instance.id, content_type=ct)


@receiver(models.signals.pre_delete, sender=Source)
def delete_source_dependencies(sender, instance, **kwargs):
    if instance.pages:
        for page in instance.pages.all():
            if page.sources:
                for sp in page.sources.all():
                    if sp.transcription:
                        sp.transcription.delete()
            page.delete()


@receiver(models.signals.post_save, sender=Transcription)
def update_source_modification(sender, instance, created, **kwargs):
    if instance.source_pages.all().exists():
        source_id = instance.source_pages.all().first().source.id
        source = Source.objects.get(pk=source_id)
        source.modification_timestamp = timezone.now()
        source.modification_user = get_current_user()
        source.save()
