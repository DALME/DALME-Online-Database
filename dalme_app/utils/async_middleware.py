from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from async_messages import get_messages


class AsyncMiddleware(MiddlewareMixin):
    """
    Fix for django-async-messages to work with newer Django versions.
    This is the same as the original middleware class with two changes:
    It uses the MiddlewareMixin for compatibility and it calls
    request.user.is_authenticated without brackets.
    """

    def process_response(self, request, response):
        """
        Check for messages for this user and, if it exists,
        call the messages API with it
        """
        if hasattr(request, "session") and hasattr(request, "user") and request.user.is_authenticated:
            msgs = get_messages(request.user)
            if msgs:
                for msg, level in msgs:
                    messages.add_message(request, level, msg)
        return response
