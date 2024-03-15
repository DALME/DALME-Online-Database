"""Model featured page data."""

import textwrap

from bs4 import BeautifulSoup as BSoup

from django.core.exceptions import ValidationError
from django.db import models

from public.models.base_image import BaseImage
from public.models.base_page import BasePage


class FeaturedPage(BasePage):
    alternate_author = models.CharField(
        max_length=127,
        null=True,
        blank=True,
        help_text='An optional name field that will be displayed as the author of this page instead of the user who created it.',
    )

    citable = models.BooleanField(
        default=True,
        help_text='Check this box to show the "Cite" menu for this page.',
    )

    front_page_image = models.ForeignKey(
        BaseImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text='The image that will display on the front page.',
    )

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

    def resolve_source_url(self):
        raise NotImplementedError

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

        if self.source_set and self.source:
            try:
                # TODO: There must be a better way to determine Set membership
                # than this but the (bi-directional) generic relations make it
                # tough. UPDATE 2023: Can't we just do this?
                #
                # if not self.source_set.members.filter(content_object__pk=self.source.pk).exists():
                #     msg = f'{self.source} is not a member of: {self.source_set}'
                #     raise ValidationError(msg) from exc
                # return super().clean()
                #
                # Let's capture it with a regression test and see.
                next(
                    source.content_object
                    for source in self.source_set.members.all()
                    if source.content_object.pk == self.source.pk
                )
            except StopIteration as exc:
                msg = f'{self.source} is not a member of: {self.source_set}'
                raise ValidationError(msg) from exc

        return super().clean()
