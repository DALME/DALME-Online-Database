"""Model for people list page."""

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.fields import StreamField

from public.extensions.extras.blocks.defaults import DEFAULT_TABLE_OPTIONS
from public.extensions.extras.blocks.document import DocumentBlock
from public.extensions.extras.blocks.subsection import SubsectionBlock
from public.extensions.extras.blocks.text_expandable import TextExpandableBlock
from public.extensions.images.blocks import InlineImageBlock, MainImageBlock
from public.extensions.team.blocks import TeamListBlock
from public.models.base_page import BasePage

BLOCK_SET = [
    ('document', DocumentBlock()),
    ('heading', blocks.CharBlock()),
    ('inline_image', InlineImageBlock()),
    ('main_image', MainImageBlock()),
    ('page', blocks.PageChooserBlock()),
    ('pullquote', blocks.RichTextBlock(icon='openquote')),
    ('subsection', SubsectionBlock()),
    ('table', TableBlock(table_options=DEFAULT_TABLE_OPTIONS)),
    ('team_list', TeamListBlock()),
    ('text', blocks.RichTextBlock()),
    ('text_expandable', TextExpandableBlock()),
]


class PeopleList(BasePage):
    template = 'public/flat.html'

    body = StreamField(BLOCK_SET, null=True)

    parent_page_types = [
        'public.Section',
        'public.Collection',
        'public.Flat',
    ]
    page_description = 'A page designed to showcase one or many people lists.'

    metadata_panels = [
        *BasePage.metadata_panels,
        FieldPanel('short_title'),
    ]
