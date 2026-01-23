"""Interface for the web.extensions.extras.blocks module."""

from .chart_embed import ChartEmbedBlock
from .code import CodeBlock
from .document import DocumentBlock
from .heading import HeadingBlock
from .subsection import SubsectionBlock
from .text_expandable import TextExpandableBlock
from .uncommented_charblock import UncommentedCharBlock

__all__ = [
    'ChartEmbedBlock',
    'CodeBlock',
    'DocumentBlock',
    'HeadingBlock',
    'SubsectionBlock',
    'TextExpandableBlock',
    'UncommentedCharBlock',
]
