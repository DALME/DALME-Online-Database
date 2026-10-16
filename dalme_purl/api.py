from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.http import HttpResponseRedirect
from dalme_app.models import Source
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
    # same visibility rule as the public site's record view (dalme_public.models)
    queryset = Source.objects.filter(workflow__is_public=True)
    # purls are public: auth for 'db'/'api' formats is enforced at the redirect target
    authentication_classes = []
    permission_classes = [AllowAny]

    def retrieve(self, request, pk=None, format=None):
        self.get_object()

        if format == 'db':
            return HttpResponseRedirect(f'{settings.DB_ENDPOINT}/sources/{pk}/')
        elif format in ['api', 'json']:
            return HttpResponseRedirect(f'{settings.API_ENDPOINT}/sources/{pk}/?format={format}')
        else:
            return HttpResponseRedirect(f'{settings.HOST_SCHEME}{settings.PARENT_HOST}/collections/records/{pk}/')
