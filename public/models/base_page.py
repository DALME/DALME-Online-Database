"""Model base page data."""

from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from django.db import models

from public.blocks import (
    BibliographyChooserBlock,
    CarouselBlock,
    ChartEmbedBlock,
    DocumentBlock,
    ExternalResourceBlock,
    FootnotesPlaceMarker,
    InlineImageBlock,
    MainImageBlock,
    PersonBlock,
    SubsectionBlock,
    SubsectionEndMarkerBlock,
)
from public.models.base_image import BaseImage
from public.models.common import HEADER_POSITION


class BasePage(Page):
    header_image = models.ForeignKey(
        BaseImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text='The image that will display in the header.',
    )
    header_position = models.CharField(
        max_length=6,
        choices=HEADER_POSITION,
        default='top',
        help_text='Position of the header image within its container.',
    )
    short_title = models.CharField(
        max_length=63,
        null=True,
        blank=True,
        help_text='An optional short title that will be displayed in certain space constrained contexts.',
    )

    body = StreamField(
        [
            ('main_image', MainImageBlock()),
            ('carousel', CarouselBlock(ImageChooserBlock())),
            ('chart_embed', ChartEmbedBlock()),
            ('inline_image', InlineImageBlock()),
            ('text', blocks.RichTextBlock()),
            ('heading', blocks.CharBlock()),
            ('pullquote', blocks.RichTextBlock(icon='openquote')),
            ('page', blocks.PageChooserBlock()),
            ('bibliography', BibliographyChooserBlock()),
            ('document', DocumentBlock()),
            ('person', PersonBlock()),
            ('external_resource', ExternalResourceBlock()),
            ('embed', EmbedBlock(icon='media')),
            ('html', blocks.RawHTMLBlock()),
            ('subsection', SubsectionBlock()),
            ('subsection_end_marker', SubsectionEndMarkerBlock()),
            ('footnotes_placemarker', FootnotesPlaceMarker()),
        ],
        null=True,
    )

    class Meta:
        abstract = True

    def get_context(self, request):
        context = super().get_context(request)
        context.update(
            {
                'header_image': self.header_image,
                'header_position': self.header_position,
            },
        )
        return context

    @property
    def main_image(self):
        try:
            field = next(field for field in self.body if field.block.name in ['carousel', 'main_image'])
        except StopIteration:
            return None
        if field.block.name == 'main_image':
            return field.value
        try:
            return field.value[0]
        except IndexError:
            return None

    @staticmethod
    def smart_truncate(content, length=25, suffix='...'):
        # credit: https://stackoverflow.com/questions/250357/truncate-a-string-without-ending-in-the-middle-of-a-word
        return content if len(content) <= length else ' '.join(content[: length + 1].split(' ')[0:-1]).rstrip() + suffix

    @property
    def title_switch(self):
        """Utility to reduce OR coalescing in templates.

        Prefer the short_title if a Page has one, if not fallback to title.

        """
        try:
            if self.short_title in ['Object', 'Essay', 'Inventory']:
                return self.smart_truncate(self.title)
        except AttributeError:
            return self.title
        else:
            return self.short_title or self.title
