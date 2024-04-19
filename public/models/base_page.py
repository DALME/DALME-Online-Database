"""Model base page data."""

from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtailcodeblock.blocks import CodeBlock

from django.db import models

from public.blocks import (
    CarouselBlock,
    ChartEmbedBlock,
    DocumentBlock,
    ExternalResourceBlock,
    InlineImageBlock,
    MainImageBlock,
    PersonBlock,
    SubsectionBlock,
    SubsectionEndMarkerBlock,
)
from public.extensions.bibliography.blocks import BibliographyChooserBlock
from public.extensions.footnotes.blocks import FootnotesPlaceMarker
from public.extensions.footnotes.models import FootnoteMixin
from public.models.base_image import BaseImage

HEADER_POSITION = (
    ('top', 'Top'),
    ('center', 'Center'),
    ('bottom', 'Bottom'),
)

DEFAULT_TABLE_OPTIONS = {
    'minSpareRows': 0,
    'startRows': 3,
    'startCols': 3,
    'colHeaders': False,
    'rowHeaders': False,
    'contextMenu': [
        'row_above',
        'row_below',
        '---------',
        'col_left',
        'col_right',
        '---------',
        'remove_row',
        'remove_col',
        '---------',
        'undo',
        'redo',
        '---------',
        'copy',
        'cut',
        '---------',
        'alignment',
    ],
    'editor': 'text',
    'stretchH': 'all',
    'height': 108,
    'renderer': 'text',
    'autoColumnSize': False,
}


DEFAULT_BLOCKS = [
    ('bibliography', BibliographyChooserBlock()),
    ('carousel', CarouselBlock(ImageChooserBlock())),
    ('chart_embed', ChartEmbedBlock()),
    ('code', CodeBlock()),
    ('document', DocumentBlock()),
    ('embed', EmbedBlock(icon='media')),
    ('external_resource', ExternalResourceBlock()),
    ('footnotes_placemarker', FootnotesPlaceMarker()),
    ('heading', blocks.CharBlock()),
    ('html', blocks.RawHTMLBlock()),
    ('inline_image', InlineImageBlock()),
    ('main_image', MainImageBlock()),
    ('page', blocks.PageChooserBlock()),
    ('person', PersonBlock()),
    ('pullquote', blocks.RichTextBlock(icon='openquote')),
    ('subsection', SubsectionBlock()),
    ('subsection_end_marker', SubsectionEndMarkerBlock()),
    ('table', TableBlock(table_options=DEFAULT_TABLE_OPTIONS)),
    ('text', blocks.RichTextBlock()),
]


class BasePage(Page, FootnoteMixin):
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

    body = StreamField(DEFAULT_BLOCKS, null=True)

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
