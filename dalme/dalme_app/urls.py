"""
URL routing is handled here
"""

from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^UIref/([a-z_-]+)$', views.uiref),
    url(r'^script/([a-z_-]+)$', views.script),
    url(r'^list/(?P<module>[a-z_-]+)(?:/(?P<type>[a-zA-Z]+))?/$', views.list),
    url(r'^form/([a-z_-]+)$', views.form),
    url(r'^show/([a-z_-]+)/([A-Za-z0-9-]+)$', views.show),
    url(r'^iiif/([a-z_-]+)$', views.iiif),
    url(r'^search/', include('haystack.urls')),
    url(r'^source/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.SourceManifest, name='source_manifest'),
    url(r'^source/(?P<pk>[a-zA-Z0-9-]+)', views.SourceDetail.as_view(), name='source_detail'),
    url(r'^source/', views.SourceList.as_view(), name='source_list'),
    url(r'^$', views.index, name='dashboard'),
]
