"""Interface for the oauth.models module."""

from __future__ import annotations

from oauth.models.application import Application
from oauth.models.group import GroupProperties
from oauth.models.user import User

__all__ = [
    'Application',
    'GroupProperties',
    'User',
]
