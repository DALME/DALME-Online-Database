from django.http import JsonResponse


class UIAuthMiddleware:
    """Update any non-authed API responses so that the UI receiver knows to
    show the reauthenticate component.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # TODO: This is brittle, must be easily improved.
        if response.status_code == 500 and not request.user.is_authenticated:
            return JsonResponse({'error': 'Reauthenticate'}, status=403)

        return response
