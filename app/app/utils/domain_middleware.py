"""Define host redirection middleware."""

from django.http import HttpResponsePermanentRedirect


class SubdomainRedirectMiddleware:
    """Middleware to redirect between subdomains."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host in ['www.dalme.org', 'public.dalme.org']:
            return HttpResponsePermanentRedirect('https://dalme.org' + request.path)
        return self.get_response(request)
