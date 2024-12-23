"""Define URLs for the oauth app."""

from oauth2_provider import urls as oauth2_urls
from oauth2_provider import views as oauth2_views

from django.urls import re_path

from oauth.api.authentication import AuthorizationCode, Login, OAuthToken
from oauth.api.csrf import csrf

app_name = 'oauth'

urls = [
    re_path(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name='authorize'),
    re_path(r'^authorize/callback/$', AuthorizationCode.as_view(), name='authorization-code'),
    re_path(r'^login/$', Login.as_view(), name='login'),
    re_path(r'^token/$', OAuthToken.as_view(), name='token'),
    re_path(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name='revoke-token'),
    re_path(r'^introspect/$', oauth2_views.IntrospectTokenView.as_view(), name='introspect'),
    re_path(r'^csrf/', csrf),
    *oauth2_urls.management_urlpatterns + oauth2_urls.oidc_urlpatterns,
]
