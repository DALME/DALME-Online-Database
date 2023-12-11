"""API endpoint exposing the CSRF token."""
from django.http import JsonResponse
from django.middleware.csrf import get_token


def csrf(request):
    """Set the CSRF token as a cookie in the browser."""
    get_token(request)
    return JsonResponse({'status': 'ok'})
