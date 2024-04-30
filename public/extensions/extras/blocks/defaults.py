"""Defaults for extra blocks."""

from wagtail import blocks
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtailcodeblock.blocks import CodeBlock

from public.extensions.bibliography.blocks import BibliographyChooserBlock
from public.extensions.footnotes.blocks import FootnotesPlaceMarker
from public.extensions.images.blocks import InlineImageBlock, MainImageBlock
from public.extensions.images.blocks.carousel import CarouselBlock
from public.extensions.team.blocks import PersonBlock

from .chart_embed import ChartEmbedBlock
from .document import DocumentBlock
from .external_resource import ExternalResourceBlock
from .text_expandable import TextExpandableBlock

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

BASE_BLOCKS = [
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
    ('table', TableBlock(table_options=DEFAULT_TABLE_OPTIONS)),
    ('text', blocks.RichTextBlock()),
    ('text_expandable', TextExpandableBlock()),
]
