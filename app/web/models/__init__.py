"""Interface for the web.models module."""

from .base_page import BasePage
from .bibliography_page import Bibliography
from .collection_page import Collection
from .collections_page import Collections
from .featured_essay_page import Essay
from .featured_inventory_page import FeaturedInventory
from .featured_object_page import FeaturedObject
from .featured_page import FeaturedPage
from .features_page import Features
from .flat_page import Flat
from .footer_links import FooterLink
from .home_page import Home
from .people_page import People
from .search_enabled_page import SearchEnabled
from .section_page import Section
from .settings import Settings
from .social_media import SocialMedia
from .sponsors import Sponsor

__all__ = [
    'BasePage',
    'Bibliography',
    'Collection',
    'Collections',
    'Essay',
    'FeaturedInventory',
    'FeaturedObject',
    'FeaturedPage',
    'Features',
    'Flat',
    'FooterLink',
    'Home',
    'People',
    'SearchEnabled',
    'Section',
    'Settings',
    'SocialMedia',
    'Sponsor',
]
