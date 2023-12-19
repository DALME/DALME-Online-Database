"""Define auth URLs for the IDA."""
from oauth2_provider import urls
from oauth2_provider import views as oauth2_views

from django.urls import include, re_path

from ida import auth

patterns = [
    re_path(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name='authorize'),
    re_path(r'^authorize/callback/$', auth.AuthorizationCode.as_view(), name='authorization-code'),
    re_path(r'^login/$', auth.Login.as_view(), name='login'),
    re_path(r'^token/$', auth.OAuthToken.as_view(), name='token'),
    re_path(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name='revoke-token'),
    re_path(r'^introspect/$', oauth2_views.IntrospectTokenView.as_view(), name='introspect'),
    *urls.management_urlpatterns + urls.oidc_urlpatterns,
]

urlpatterns = [
    re_path(r'^', include(patterns)),
]
