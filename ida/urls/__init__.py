"""Interface for the ida.urls module."""
from django.urls import include, re_path

from .auth import urlpatterns as auth_urlpatterns

urlpatterns = [
    re_path(r'^oauth/', include((auth_urlpatterns, 'ida'), namespace='oauth2_provider')),
]
