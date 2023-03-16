"""Define the multiple proxy middleware."""


class MultipleProxyMiddleware:
    """Ensure `request.get_host` works after passing through multiple proxies.

    Probably not strictly necessary for the time being, but worth reinforcing
    as our multitenancy solution is absolutely dependent on receiving the
    correct value from `get_host` in order to function correctly.

    """

    FORWARDED_FOR_FIELDS = [
        "HTTP_X_FORWARDED_FOR",
        "HTTP_X_FORWARDED_HOST",
        "HTTP_X_FORWARDED_SERVER",
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Rewrite proxy headers so that only the original host is used."""
        for field in self.FORWARDED_FOR_FIELDS:
            if field in request.META and "," in request.META[field]:
                host, *_ = request.META[field].split(",")
                request.META[field] = host.strip()

        return self.get_response(request)
