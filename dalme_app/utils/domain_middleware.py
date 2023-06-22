from django.http import HttpResponsePermanentRedirect


class SubdomainRedirectMiddleware:
    """Middleware to redirect between subdomains."""

    def __init__(self, get_response):  # noqa: D107
        self.get_response = get_response

    def __call__(self, request):  # noqa: D102
        host = request.get_host()
        if host in ['www.dalme.org', 'public.dalme.org']:
            return HttpResponsePermanentRedirect('https://dalme.org' + request.path)
        if host in ['www.127.0.0.1.sslip.io:8000', 'public.127.0.0.1.sslip.io:8000']:
            return HttpResponsePermanentRedirect('https://127.0.0.1.sslip.io:8000' + request.path)
        return self.get_response(request)
