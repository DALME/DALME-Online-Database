"""Interface for the web.extensions.extras.blocks module."""

from web.extensions.images.blocks import CarouselBlock, InlineImageBlock

from .chart_embed import ChartEmbedBlock
from .defaults import DEFAULT_TABLE_OPTIONS
from .document import DocumentBlock
from .heading import HeadingBlock
from .text_expandable import TextExpandableBlock
from .uncommented_charblock import UncommentedCharBlock


def get_default_blocks():
    from .defaults import BASE_BLOCKS
    from .subsection import SubsectionBlock

    return sorted([*BASE_BLOCKS, ('subsection', SubsectionBlock())], key=lambda x: x[0])


__all__ = [
    'DEFAULT_TABLE_OPTIONS',
    'CarouselBlock',
    'ChartEmbedBlock',
    'DocumentBlock',
    'HeadingBlock',
    'InlineImageBlock',
    'SubsectionBlock',
    'TextExpandableBlock',
    'UncommentedCharBlock',
    'get_default_blocks',
]
