"""Define an interface for late-bound access to StreamField blocks."""

from wagtail.fields import StreamField

STREAMFIELD_INTERFACE = [
    'bibliography',
    'carousel',
    'chart_embed',
    'code',
    'document',
    'embed',
    'footnotes_placemarker',
    'heading',
    'html',
    'inline_image',
    'page',
    'pullquote',
    'subsection',
    'table',
    'table_typed',
    'text',
    'text_expandable',
]

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
    'language': 'en-US',
    'height': 108,
    'renderer': 'text',
    'autoColumnSize': False,
}


class BlockRegistry:
    """Late-binding factory for generating StreamField block definitions."""

    @classmethod
    def block_def(cls, blocks):
        """Derive an arbitrary StreamField block definition.

        The arg 'blocks' must be a list of strings mapping to methods on this
        class.
        """
        try:
            return [(block, getattr(cls, block)()) for block in sorted(blocks)]
        except TypeError:
            # Sometimes StreamField mutates the block list data somewhere
            # (obscure that I can't detect) so we need to handle that case.
            return [(block[0], getattr(cls, block[0])()) for block in sorted(blocks)]

    @staticmethod
    def bibliography():
        from web.extensions.bibliography.blocks import BibliographyChooserBlock

        return BibliographyChooserBlock()

    @staticmethod
    def carousel():
        from wagtail.images.blocks import ImageChooserBlock

        from web.extensions.images.blocks.carousel import CarouselBlock

        return CarouselBlock(ImageChooserBlock())

    @staticmethod
    def chart_embed():
        from web.extensions.extras.blocks import ChartEmbedBlock

        return ChartEmbedBlock()

    @staticmethod
    def code():
        from web.extensions.extras.blocks import CodeBlock

        return CodeBlock()

    @staticmethod
    def document():
        from web.extensions.extras.blocks import DocumentBlock

        return DocumentBlock()

    @staticmethod
    def embed():
        from wagtail.embeds.blocks import EmbedBlock

        return EmbedBlock(icon='media')

    @staticmethod
    def footnotes_placemarker():
        from web.extensions.footnotes.blocks import FootnotesPlaceMarker

        return FootnotesPlaceMarker()

    @staticmethod
    def heading():
        from web.extensions.extras.blocks.heading import HeadingBlock

        return HeadingBlock()

    @staticmethod
    def html():
        from wagtail.blocks import RawHTMLBlock

        return RawHTMLBlock()

    @staticmethod
    def inline_image():
        from web.extensions.images.blocks import InlineImageBlock

        return InlineImageBlock()

    @staticmethod
    def page():
        from wagtail.blocks import PageChooserBlock

        return PageChooserBlock()

    @staticmethod
    def pullquote():
        from wagtail.blocks import RichTextBlock

        return RichTextBlock(icon='openquote', editor='minimal')

    @staticmethod
    def subsection():
        from web.extensions.extras.blocks.subsection import SubsectionBlock

        return SubsectionBlock()

    @staticmethod
    def table():
        from wagtail.contrib.table_block.blocks import TableBlock

        return TableBlock(table_options=DEFAULT_TABLE_OPTIONS, icon='table-cells', form_classname='table-block')

    @staticmethod
    def table_typed():
        from wagtail.blocks import CharBlock, FloatBlock, RichTextBlock
        from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
        from wagtail.images.blocks import ImageBlock

        return TypedTableBlock(
            [
                ('text', CharBlock()),
                ('numeric', FloatBlock()),
                ('rich_text', RichTextBlock()),
                ('image', ImageBlock()),
            ],
            label='Table (typed)',
        )

    @staticmethod
    def team_list():
        from web.extensions.team.blocks import TeamListBlock

        return TeamListBlock()

    @staticmethod
    def text():
        from wagtail.blocks import RichTextBlock

        return RichTextBlock(editor='minimal')

    @staticmethod
    def text_expandable():
        from web.extensions.extras.blocks import TextExpandableBlock

        return TextExpandableBlock()


class RegistryStreamField(StreamField):
    """Allow defining a StreamField via the block registry.

    This helps prevent us from getting into circular import hell, something
    which is easily done with StreamField blocks and top-level imports.

    """

    def __init__(self, block_types, **kwargs):
        """Initialize a LazyStreamField.

        Block types must be a list of strings and the full block def will be
        derived from the registry above.

        """
        block_types = BlockRegistry.block_def(block_types)
        super().__init__(block_types, **kwargs)
