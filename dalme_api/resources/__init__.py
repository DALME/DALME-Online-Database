"""Interface for the dalme_api.resources module."""
from .agents import Agents
from .attachments import Attachments
from .attributes import Attributes, AttributeTypes, ContentTypes
from .collections import Collections
from .comments import Comments
from .countries import Countries
from .datasets import Datasets
from .groups import Groups
from .images import Images
from .languages import Languages
from .library import Library
from .locales import Locales
from .locations import Locations
from .pages import Pages
from .ping import Ping
from .places import Places
from .records import Records
from .rights import Rights
from .session import Session
from .tasks import TaskLists, Tasks
from .tickets import Tickets
from .transcriptions import Transcriptions
from .users import Users
from .workflows import Workflows

__all__ = [
    'Agents',
    'Attachments',
    'AttributeTypes',
    'Attributes',
    'Collections',
    'Comments',
    'ContentTypes',
    'Countries',
    'Datasets',
    'Groups',
    'Images',
    'Languages',
    'Library',
    'Locales',
    'Locations',
    'Pages',
    'Ping',
    'Places',
    'Records',
    'Rights',
    'Session',
    'TaskLists',
    'Tasks',
    'Tickets',
    'Transcriptions',
    'Users',
    'Workflows',
]