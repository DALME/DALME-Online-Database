"""Interface for the data fixtures for the migrate_data management command."""

from .attribute_types import ATYPES_KEEP, NEW_TYPES, RENAMES, TO_BOOL, TO_FKEY, TO_INT, TO_LOCAL, TO_RREL
from .attributes import DUPLICATES
from .bibliography import COLLECTIONS, REF_CITATIONS
from .ct_attributes_map import CT_DATA, CTA_PROPS
from .gradients import GRADIENTS
from .locales import NEW_LOCALES, PLACE_CONCORDANCE
from .maps import ALTERED_APP_MAP, ALTERED_MODEL_MAP, SOURCES_MODEL_MAP
from .named_agents import NAMED_AGENTS, UNATTACHED_AGENTS
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
from .rs_tag_data import (
    CONTENT_CLEANUP_EXPRESSIONS,
    ONE_OFF_TRANSFORMS,
    ORG_NAME_PATTERNS,
    PERSONAL_NAME_PATTERNS,
    REMOVAL_MATCHES,
    RS_TYPES,
)
from .tei_elements import TEI_ATTRIBUTE_OPTIONS, TEI_ELEMENTS

__all__ = [
    'ABOUT_DATA',
    'ABOUT_FLAT_DATA',
    'ALTERED_APP_MAP',
    'ALTERED_MODEL_MAP',
    'ATYPES_KEEP',
    'COLLECTIONS',
    'CONTENT_CLEANUP_EXPRESSIONS',
    'CTA_PROPS',
    'CT_DATA',
    'DEFAULT_PREFERENCES',
    'DEFAULT_SETTINGS',
    'DUPLICATES',
    'GRADIENTS',
    'HOME_DATA',
    'NAMED_AGENTS',
    'NAMED_AGENTS',
    'NEW_LOCALES',
    'NEW_TYPES',
    'ONE_OFF_TRANSFORMS',
    'OPTIONS',
    'ORG_NAME_PATTERNS',
    'PEOPLE_PAGE_DATA',
    'PERSONAL_NAME_PATTERNS',
    'PLACE_CONCORDANCE',
    'PROJECT_DATA',
    'PROJECT_FLAT_DATA',
    'RECORD_TYPES',
    'RECORD_TYPE_COVERSIONS',
    'REF_CITATIONS',
    'REMOVAL_MATCHES',
    'RENAMES',
    'ROLES',
    'RS_TYPES',
    'SAMPLE_GRADIENTS',
    'SOURCES_MODEL_MAP',
    'TEI_ATTRIBUTE_OPTIONS',
    'TEI_ELEMENTS',
    'TO_BOOL',
    'TO_FKEY',
    'TO_INT',
    'TO_LOCAL',
    'TO_RREL',
    'UNATTACHED_AGENTS',
    'USER_NAME_CONCORDANCE',
]
