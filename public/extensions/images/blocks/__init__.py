"""Interface for the public.extensions.images.blocks module."""

from .carousel import CarouselBlock
from .inline_image import InlineImageBlock
from .main_image import MainImageBlock

__all__ = [
    'CarouselBlock',
    'InlineImageBlock',
    'MainImageBlock',
]
