"""Add values to the template context for public."""

from datetime import datetime

from django.utils import timezone


def year(request):  # noqa: ARG001
    """Return current year."""
    return {'year': datetime.now(tz=timezone.get_current_timezone()).year}


def project(request):  # noqa: ARG001
    """Return project name."""
    return {'project': 'The Documentary Archaeology of Late Medieval Europe'}
