"""Interface for the public.extensions.extra_blocks.blocks module."""

from public.extensions.images.blocks import CarouselBlock, InlineImageBlock, MainImageBlock
from public.extensions.team.blocks import PersonBlock

from .chart_embed import ChartEmbedBlock
from .defaults import BASE_BLOCKS, DEFAULT_TABLE_OPTIONS
from .document import DocumentBlock
from .external_resource import ExternalResourceBlock
from .subsection import SubsectionBlock
from .text_expandable import TextExpandableBlock

DEFAULT_BLOCKS = [
    *BASE_BLOCKS,
    ('subsection', SubsectionBlock()),
]

__all__ = [
    'CarouselBlock',
    'ChartEmbedBlock',
    'DocumentBlock',
    'ExternalResourceBlock',
    'InlineImageBlock',
    'MainImageBlock',
    'PersonBlock',
    'TextExpandableBlock',
    'SubsectionBlock',
    'DEFAULT_TABLE_OPTIONS',
    'DEFAULT_BLOCKS',
]
