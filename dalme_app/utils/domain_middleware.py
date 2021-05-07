from django.http import HttpResponsePermanentRedirect


class SubdomainRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host()
        if host in ['www.dalme.org', 'public.dalme.org']:
            return HttpResponsePermanentRedirect('https://dalme.org' + request.path)
        if host in ['www.127.0.0.1.sslip.io:8443', 'public.127.0.0.1.sslip.io:8443']:
            return HttpResponsePermanentRedirect('https://127.0.0.1.sslip.io:8443' + request.path)
        return self.get_response(request)
