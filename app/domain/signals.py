"""Define ORM signals for the domain."""

import os

from django_currentuser.middleware import get_current_user
from wagtail.search import index
from wagtail.search.signal_handlers import post_delete_signal_handler, post_save_signal_handler

from django.contrib.contenttypes.models import ContentType
from django.db import connection, models
from django.dispatch import receiver
from django.utils import timezone

from oauth.models import User
from tenants.models import Tenant

from .models import (
    Page,
    PageNode,
    Preference,
    PreferenceKey,
    PublicRegister,
    Record,
    Transcription,
    Workflow,
    WorkLog,
    rs_resource,
)

models.signals.post_save.disconnect(post_save_signal_handler, sender=Record)
models.signals.post_delete.connect(post_delete_signal_handler, sender=Record)


@receiver(models.signals.post_save, sender=Page)
def page_post_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """Run after save method on Page objects."""
    if instance.dam_id is not None and not os.environ.get('DATA_MIGRATION'):
        rs_image = rs_resource.objects.get(ref=instance.dam_id)
        rs_image.field79 = instance.name
        rs_image.save()


@receiver(models.signals.post_save, sender=Record)
def record_post_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """Run after save method on Record objects."""
    if not os.environ.get('DATA_MIGRATION'):
        # Create workflow record if this is a new source.
        if created:
            wf = Workflow(
                record=instance,
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
def record_pre_delete(sender, instance, **kwargs):  # noqa: ARG001
    """Run before delete method on Record objects."""
    if not os.environ.get('DATA_MIGRATION'):
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
    if instance.pagenodes.exists() and not os.environ.get('DATA_MIGRATION'):
        for node in instance.pagenodes.all():
            record = node.record

            # Update source tracking.
            record.modification_timestamp = timezone.now()
            record.modification_user = get_current_user()
            record.save()

            # Emit the post_save signal on page_node for indexing purposes.
            models.signals.post_save.send(sender=PageNode, instance=node, created=False)


@receiver(models.signals.post_save, sender=Record)
def wagtail_index_post_save_signal_handler(instance, update_fields=None, **kwargs):  # noqa: ARG001
    """Update Wagtail search index after save method on Record objects."""
    if update_fields is not None:
        # fetch a fresh copy of instance from the database to ensure
        # that we're not indexing any of the unsaved data contained in
        # the fields that were not passed in update_fields
        instance = type(instance).objects.get(pk=instance.pk)

    for tenant in Tenant.objects.exclude(schema_name='public').all():
        connection.set_tenant(tenant)
        index.insert_or_update_object(instance)


@receiver(models.signals.post_delete, sender=Record)
def wagtail_index_post_delete_signal_handler(instance, **kwargs):  # noqa: ARG001
    """Update Wagtail search index after delete method on Record objects."""
    for tenant in Tenant.objects.exclude(schema_name='public').all():
        connection.set_tenant(tenant)
        index.remove_object(instance)


@receiver(models.signals.post_save, sender=Workflow)
def workflow_post_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """Run after save method on Workflow objects."""
    if not os.environ.get('DATA_MIGRATION'):
        if not created:
            models.signals.post_save.send(sender=Record, instance=instance.record, created=False)
        else:
            WorkLog.objects.update_or_create(record=instance, event='Record created', timestamp=instance.last_modified)


@receiver(models.signals.post_save, sender=PreferenceKey)
def preference_key_post_save(sender, instance, created, **kwargs):  # noqa: ARG001
    """Run after save method on PreferenceKey objects to add new pref to users."""
    if created:
        preferences = [Preference(user=i, key=instance, data=instance.default) for i in User.objects.all()]
        Preference.objects.bulk_create(preferences)
