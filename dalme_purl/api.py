"""Define endpoints for dalme_purl."""
from rest_framework import viewsets

from django.conf import settings
from django.http import HttpResponseRedirect

from ida.models import PublicRegister


class Endpoint(viewsets.GenericViewSet):
    """Permanent URL endpoint for DALME.

    Accepts the following formats:

    None -> Redirect to public website.
    db -> Redirect to db.dalme (if session present and auth/permission checks pass).
    api -> Redirect to API View in db.dalme, subject to same checks as above.
    json -> JSON response.
    json-p -> JSON-P response.

    """

    queryset = PublicRegister.objects.all()

    def retrieve(self, request, pk=None, fmt=None):  # noqa: ARG002
        """Get individual record."""
        self.get_object()

        if format == 'db':
            return HttpResponseRedirect(f'{settings.HOST}/db/sources/{pk}/')

        if format in ['api', 'json']:
            return HttpResponseRedirect(
                f'{settings.HOST}/api/sources/{pk}/?format={fmt}',
            )

        return HttpResponseRedirect(f'{settings.HOST}/collections/records/{pk}/')
