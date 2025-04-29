"""Model featured page data."""

import textwrap

from bs4 import BeautifulSoup as BSoup
from wagtail.admin.panels import FieldPanel

from django.core.exceptions import ValidationError
from django.db import models

from web.extensions.analytics.models import AnalyticsMixin
from web.extensions.bibliography.models import CitableMixin
from web.extensions.images.models import BaseImage
from web.extensions.team.models import BylineMixin
from web.models.base_page import BasePage


class FeaturedPage(BasePage, CitableMixin, BylineMixin, AnalyticsMixin):
    front_page_image = models.ForeignKey(
        BaseImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='The image to use on the front page when this page is featured.',
    )

    metadata_panels = [
        *BasePage.metadata_panels,
        *CitableMixin.metadata_panels,
        *BylineMixin.metadata_panels,
        FieldPanel('front_page_image'),
    ]

    class Meta:
        abstract = True

    def get_context(self, request):
        context = super().get_context(request)
        context['feature_type'] = self.short_title
        return context

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
