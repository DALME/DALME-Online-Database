from rest_framework import viewsets
from django.http import HttpResponseRedirect
from dalme_app.models import PublicRegister
from django.conf import settings


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
            return HttpResponseRedirect(f'{settings.DB_ENDPOINT}/sources/{pk}/')
        elif format in ['api', 'json']:
            return HttpResponseRedirect(f'{settings.API_ENDPOINT}/sources/{pk}/?format={format}')
        else:
            return HttpResponseRedirect(f'{settings.HOST_SCHEME}{settings.PARENT_HOST}/collections/records/{pk}/')
