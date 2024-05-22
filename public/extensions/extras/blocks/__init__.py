"""Interface for the public.extensions.extras.blocks module."""

from public.extensions.images.blocks import CarouselBlock, InlineImageBlock

from .chart_embed import ChartEmbedBlock
from .defaults import BASE_BLOCKS, DEFAULT_TABLE_OPTIONS
from .document import DocumentBlock
from .subsection import SubsectionBlock
from .text_expandable import TextExpandableBlock

DEFAULT_BLOCKS = sorted([*BASE_BLOCKS, ('subsection', SubsectionBlock())], key=lambda x: x[0])

__all__ = [
    'CarouselBlock',
    'ChartEmbedBlock',
    'DocumentBlock',
    'InlineImageBlock',
    'TextExpandableBlock',
    'SubsectionBlock',
    'DEFAULT_TABLE_OPTIONS',
    'DEFAULT_BLOCKS',
]
