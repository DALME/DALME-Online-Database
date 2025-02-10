"""Signals for team extension."""

from wagtail.users.models import UserProfile

from django.core.files.storage import FileSystemStorage
from django.db.models.signals import pre_save
from django.dispatch import receiver


@receiver(pre_save, sender=UserProfile, dispatch_uid='handle_avatar_image')
def handle_avatar_image(sender, **kwargs):  # noqa: ARG001
    """Prevent django-tenants from adding tenant directory to image.

    The UserProfile model is not tenantized, and avatar images are saved to
    a directory that is not tenant-specific, however django-tenants will add
    the tenant to the path regardless. We stop it by overriding the storage attribute
    in the field's class with Django's default storage module.
    """
    instance = kwargs.get('instance')
    if instance.avatar:
        instance.avatar.storage = FileSystemStorage()
