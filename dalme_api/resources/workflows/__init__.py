"""Interface for the dalme_api.resources.workflows module."""
from .endpoints import Workflows
from .serializers import WorkflowSerializer

__all__ = [
    'WorkflowSerializer',
    'Workflows',
]
