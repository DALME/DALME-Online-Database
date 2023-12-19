"""Extend the default OAuth application model."""
from oauth2_provider.models import AbstractApplication

from django.db import models


class Application(AbstractApplication):
    """Model an OAuth application representing an OAuth Client.

    An OAuth Client is an application authorized to access OAuth2-protected
    resources on behalf of a resource owner.

    """

    logo = models.ImageField(blank=True, null=True)
