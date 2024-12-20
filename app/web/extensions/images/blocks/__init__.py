"""Interface for the web.extensions.images.blocks module."""

from .carousel import CarouselBlock
from .inline_image import InlineImageBlock

__all__ = [
    'CarouselBlock',
    'InlineImageBlock',
]
