"""Interface for the web.extensions.extras.blocks module."""

from web.extensions.images.blocks import CarouselBlock, InlineImageBlock

from .chart_embed import ChartEmbedBlock
from .defaults import BASE_BLOCKS, DEFAULT_TABLE_OPTIONS
from .document import DocumentBlock
from .heading import HeadingBlock
from .subsection import SubsectionBlock
from .text_expandable import TextExpandableBlock
from .uncommented_charblock import UncommentedCharBlock

DEFAULT_BLOCKS = sorted([*BASE_BLOCKS, ('subsection', SubsectionBlock())], key=lambda x: x[0])

__all__ = [
    'DEFAULT_BLOCKS',
    'DEFAULT_TABLE_OPTIONS',
    'CarouselBlock',
    'ChartEmbedBlock',
    'DocumentBlock',
    'HeadingBlock',
    'InlineImageBlock',
    'SubsectionBlock',
    'TextExpandableBlock',
    'UncommentedCharBlock',
]
