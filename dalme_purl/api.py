from rest_framework import viewsets
from django.http import HttpResponseRedirect
from dalme_app.models import PublicRegister


class Endpoint(viewsets.GenericViewSet):
    """
        PURL/Stable endpoint for DALME. Formats:
        no format -> redirects to public website
        'db' -> redirects to db.dalme, subject to session being present in request and it passing auth/permission checks
        'api' -> to api view in db.dalme, subject to same checks
        'json' -> json response
        'json-p' -> json-p response
    """
    queryset = PublicRegister.objects.all()

    def retrieve(self, request, pk=None, format=None):
        self.get_object()

        if format == 'db':
            return HttpResponseRedirect(f'https://db.127.0.0.1.xip.io:8443/sources/{pk}/')
        elif format == 'api':
            return HttpResponseRedirect(f'https://data.127.0.0.1.xip.io:8443/sources/{pk}/?format=api')
        else:
            return HttpResponseRedirect(f'https://public.127.0.0.1.xip.io:8443/collections/records/{pk}/')
