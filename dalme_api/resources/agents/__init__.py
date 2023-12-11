"""Interface for the dalme_api.resources.agents module."""
from .endpoints import Agents
from .serializers import AgentSerializer

__all__ = [
    'AgentSerializer',
    'Agents',
]
