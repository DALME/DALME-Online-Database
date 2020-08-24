from threading import local
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from async_messages import get_messages
from rest_framework import permissions
from djangosaml2idp.processors import BaseProcessor
from typing import Dict

# MIDDLEWARE
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


# OIDC Provider Settings
# def oidc_userinfo(claims, user):
#     # Populate claims dict.
#     claims['name'] = '{0} {1}'.format(user.first_name, user.last_name)
#     claims['given_name'] = user.first_name
#     claims['family_name'] = user.last_name
#     claims['email'] = user.email
#     claims['address']['street_address'] = '...'
#     claims['preferred_username'] = user.username
#     return claims


# BasePermission Override to implement per-ownership permission_classes
class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Object-level permission to only allow owners of an object to edit it. """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.owner == request.user or request.user.is_superuser:
            return True
        else:
            return False


# Routers to support external databases (WP, DAM, Wiki)
class ModelDatabaseRouter(object):
    """Allows each model to set its own db target"""

    def db_for_read(self, model, **hints):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return None

    def db_for_write(self, model, **hints):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return None

    def allow_syncdb(self, db, model):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            if model._meta.in_db == db:
                return True
            else:
                return False
        else:
            # Random models that don't specify a database can only go to 'default'
            if db == 'default':
                return True
            else:
                return False


# djangosaml2idp processor
class SAMLProcessor(BaseProcessor):
    """ subclasses the default djangosaml2idp processor
    to allow for special fields to be included in response """

    def create_identity(self, user, sp_attribute_mapping: Dict[str, str]) -> Dict[str, str]:
        results = {}
        for user_attr, out_attr in sp_attribute_mapping.items():
            attr_lst = user_attr.split('.')
            if len(attr_lst) > 1 and attr_lst[0] == 'profile':
                results[out_attr] = getattr(user.profile, attr_lst[1])
            if user_attr == 'groups':
                results[out_attr] = user.groups.values_list('name', flat=True)
            # elif user_attr == 'profile_image':
            #     results[out_attr] = user.profile.profile_image
            elif hasattr(user, user_attr):
                attr = getattr(user, user_attr)
                results[out_attr] = attr() if callable(attr) else attr
        return results
