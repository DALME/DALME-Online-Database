"""Models for team extension."""

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.functions import Lower
from django.template.defaultfilters import slugify

from domain.models import Avatar
from web.extensions.team.widgets import AuthorSelect


class TeamRole(models.Model):
    role = models.CharField(max_length=255, unique=True, help_text='Name of the role.')
    description = models.TextField(help_text='Description of the role.')
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='Parent role, if any.',
    )

    class Meta:
        ordering = ['-parent__role', '-role']

    def __str__(self):
        return f'{self.role} ({self.parent.role})' if self.parent else f'{self.role}'


class TeamMember(Avatar):
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

    class Meta:
        constraints = [
            models.UniqueConstraint(name='unique_user', fields=['user'], nulls_distinct=True),
            models.UniqueConstraint('name', Lower('title'), name='unique_name_lower_title'),
        ]

    def __str__(self):
        return str(self.name)


class BylineMixin(models.Model):
    authors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        help_text='Users to include in the byline. Adding authors to this field also ensures this page will show in their listed contributions.',
    )
    byline_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='The text to be shown on the frontend. This field will be auto-generated from the users linked above, but it can be edited manually.',
    )

    metadata_panels = [
        MultiFieldPanel(
            [
                FieldPanel(
                    'authors',
                    widget=AuthorSelect(
                        placeholder='Select authors...',
                        sortable=True,
                        api_state='userSelectState',
                        queryset=get_user_model().objects.all(),
                    ),
                ),
                FieldPanel('byline_text'),
            ],
            heading='Byline',
            icon='users-line',
            help_text='This section allows you to customize the byline for this page (by default, the user who created it will be shown as the author).',
        )
    ]

    class Meta:
        abstract = True

    @property
    def byline(self):
        if self.byline_text:
            return self.byline_text
        return self.owner.full_name

    @property
    def byline_url(self):
        if self.byline_text:
            return None
        return slugify(self.owner.full_name)
