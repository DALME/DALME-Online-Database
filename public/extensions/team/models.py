"""Models for team extension."""

import io

from wagtail.fields import RichTextField

from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.functions import Lower


class TeamRole(models.Model):
    role = models.CharField(max_length=255, help_text='Name of the role.')
    description = models.TextField(help_text='Description of the role.')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='Parent role, if any.',
    )

    def __str__(self):
        return f'{self.role} ({self.parent.role})' if self.parent else f'{self.role}'


class TeamMember(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='team_member_record',
        blank=True,
        null=True,
        help_text='Associated user record, if any.',
    )
    name = models.CharField(max_length=255, help_text='Name as it should appear on the front end.')
    roles = models.ManyToManyField(TeamRole, blank=True, help_text='Project role(s).')
    title = models.CharField(max_length=255, blank=True, help_text='Professional title(s).')
    affiliation = models.CharField(max_length=255, blank=True, help_text='Institutional affiliation.')
    biography = RichTextField(
        features=[
            'bold',
            'italic',
            'link',
            'document-link',
            'code',
            'superscript',
            'subscript',
            'strikethrough',
            'blockquote',
            'reference',
        ],
        blank=True,
        help_text='Short biographical sketch.',
    )
    url = models.URLField(
        blank=True,
        verbose_name='Website',
        help_text='Link to a website or online profile.',
    )
    photo = models.ForeignKey(
        'publicimages.BaseImage',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='Profile image or avatar.',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_user', fields=['user'], nulls_distinct=True),
            models.UniqueConstraint('name', Lower('title'), name='unique_name_lower_title'),
        ]

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        """Override the save method to save avatar image if this is a user adding a photo."""
        if self.user and self.photo:
            profile_obj = self.user.wagtail_userprofile
            # django-tenants will try to add the tenant to the path
            # to prevent it, we override the "storage" attribute of
            # the field class with Django's default storage model
            profile_obj.avatar.storage = FileSystemStorage()
            profile_obj.avatar.save(
                self.photo.title,
                File(io.BytesIO(self.photo.file.read())),
            )
            profile_obj.save()
            self.photo = None
        return super().save(*args, **kwargs)

    @property
    def avatar(self):
        if self.user:
            return self.user.wagtail_userprofile.avatar
        return self.photo.file if self.photo else None
