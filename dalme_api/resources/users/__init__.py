"""Interface for the dalme_api.resources.users module."""
from .endpoints import Users
from .serializers import UserSerializer

__all__ = [
    'UserSerializer',
    'Users',
]
