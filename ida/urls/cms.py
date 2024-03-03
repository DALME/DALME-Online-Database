"""Define wagtail cms URLs for the IDA."""

from wagtail.admin import urls as wagtailadmin_urls

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import include, re_path, reverse

admin.site.unregister(Group)


def to_ida_login(_request):
    """Redirect request to login page."""
    return auth_views.redirect_to_login(reverse('wagtailadmin_home'), login_url=settings.LOGIN_URL)


def to_ida_logout(_request):
    """Redirect request to logout page."""
    return redirect(settings.LOGOUT_URL)


patterns = [
    re_path('cms/login/', to_ida_login, name='wagtailadmin_login'),
    re_path('cms/logout/', to_ida_logout, name='wagtailadmin_logout'),
    re_path(r'^', include(wagtailadmin_urls)),
]

urlpatterns = [
    re_path(r'^', include(patterns)),
]
