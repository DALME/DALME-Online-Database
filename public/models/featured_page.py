"""Model featured page data."""

import textwrap

from bs4 import BeautifulSoup as BSoup
from wagtail.admin.panels import FieldPanel

from django.core.exceptions import ValidationError
from django.db import models

from public.extensions.bibliography.models import CitableMixin
from public.models.base_image import BaseImage
from public.models.base_page import BasePage


class FeaturedPage(BasePage, CitableMixin):
    alternate_author = models.CharField(
        max_length=127,
        null=True,
        blank=True,
        help_text='An optional name field that will be displayed as the author of this page instead of the user who created it.',
    )
    front_page_image = models.ForeignKey(
        BaseImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='The image that will display on the front page.',
    )

    content_panels = [
        *BasePage.content_panels,
        *CitableMixin.content_panels,
        FieldPanel('front_page_image'),
        FieldPanel('alternate_author'),
    ]

    class Meta:
        abstract = True

    def get_context(self, request):
        context = super().get_context(request)
        context['feature_type'] = self.short_title
        return context

    @property
    def author(self):
        if self.alternate_author:
            return self.alternate_author
        return self.owner.profile.full_name

    @property
    def scheduled_publication(self):
        revisions = self.revisions.filter(approved_go_live_at__isnull=False).order_by('-created_at')
        if revisions.exists():
            return revisions.first().approved_go_live_at  # .strftime('%d-%b-%Y@%H:%M')
        return None

    @property
    def front_image(self):
        return self.front_page_image or self.main_image

    def snippet(self, width=200):
        try:
            text = next(field for field in self.body if field.block.name == 'text')
        except StopIteration:
            return ''
        return textwrap.shorten(
            BSoup(text.value.source, 'html.parser').get_text(),
            width=width,
            placeholder='...',
        )

    def clean(self):
        if self.go_live_at:
            qs = self._meta.model.objects.filter(
                go_live_at=self.go_live_at,
            ).exclude(pk=self.pk)
            if qs.exists():
                model = self._meta.label.split('.')[-1]
                title = qs.first().title
                msg = f'{model}: {title} is already scheduled for publication at: {self.go_live_at}'
                raise ValidationError(msg)

        return super().clean()
