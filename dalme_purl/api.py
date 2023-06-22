from rest_framework import viewsets

from django.conf import settings
from django.http import HttpResponseRedirect

from dalme_app.models import PublicRegister


class Endpoint(viewsets.GenericViewSet):
    """Permanent URL endpoint for DALME.

    Formats:
        no format -> redirects to public website
        db -> redirects to db.dalme, subject to session must be in request and pass auth/permission checks
        api -> to api view in db.dalme, subject to same checks
        json -> returns json response
        json-p -> returns json-p response.
    """

    queryset = PublicRegister.objects.all()

    def retrieve(self, request, pk=None, fmt=None):  # noqa: ARG002
        """Get individual record."""
        self.get_object()
        path = (
            f'/db/sources/{pk}/'
            if fmt == 'db'
            else f'/api/sources/{pk}/?format={fmt}'
            if fmt in ['api', 'json']
            else f'/collections/records/{pk}/'
        )
        return HttpResponseRedirect(f'{settings.HOST}{path}')
