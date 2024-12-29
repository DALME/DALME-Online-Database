"""Interface for the data fixtures for the migrate_data management command."""

from .attribute_types import ATYPES_KEEP, TO_BOOL, TO_FKEY, TO_INT, TO_LOCAL, TO_RREL
from .bibliography import COLLECTIONS, REF_CITATIONS
from .ct_attributes_map import CT_DATA, CTA_PROPS
from .gradients import GRADIENTS
from .maps import ALTERED_APP_MAP, ALTERED_MODEL_MAP, SOURCES_MODEL_MAP
from .named_agents import NAMED_AGENTS
from .options import OPTIONS
from .people import PEOPLE_PAGE_DATA, ROLES, USER_NAME_CONCORDANCE
from .pharma_web import (
    ABOUT_DATA,
    ABOUT_FLAT_DATA,
    DEFAULT_SETTINGS,
    HOME_DATA,
    PROJECT_DATA,
    PROJECT_FLAT_DATA,
    SAMPLE_GRADIENTS,
)
from .preferences import DEFAULT_PREFERENCES
from .record_types import RECORD_TYPE_COVERSIONS, RECORD_TYPES

__all__ = [
    'ABOUT_DATA',
    'ABOUT_FLAT_DATA',
    'ALTERED_APP_MAP',
    'ALTERED_MODEL_MAP',
    'ATYPES_KEEP',
    'COLLECTIONS',
    'CTA_PROPS',
    'CT_DATA',
    'DEFAULT_PREFERENCES',
    'DEFAULT_SETTINGS',
    'GRADIENTS',
    'HOME_DATA',
    'NAMED_AGENTS',
    'OPTIONS',
    'PEOPLE_PAGE_DATA',
    'PROJECT_DATA',
    'PROJECT_FLAT_DATA',
    'RECORD_TYPES',
    'RECORD_TYPE_COVERSIONS',
    'REF_CITATIONS',
    'ROLES',
    'SAMPLE_GRADIENTS',
    'SOURCES_MODEL_MAP',
    'TO_BOOL',
    'TO_FKEY',
    'TO_INT',
    'TO_LOCAL',
    'TO_RREL',
    'USER_NAME_CONCORDANCE',
]
