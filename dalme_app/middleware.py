from threading import local
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from async_messages import get_messages

_user = local()


class CurrentUserMiddleware(object):
    """
    Enables setting user or usename as default values in models.py.
    Used to automatically set creation and modification records.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.__setattr__('username', request.user.username)
        _user.__setattr__('user', request.user)
        return self.get_response(request)


def get_current_username():
    return _user.__getattribute__('username')


def get_current_user():
    return _user.__getattribute__('user')


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
