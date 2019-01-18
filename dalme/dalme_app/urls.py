"""
URL routing is handled here
"""
from django.urls import path, re_path, include
from django.contrib import admin
from . import views

urlpatterns = [
    re_path(r'^UIref/([a-z_-]+)$', views.uiref, name='uiref'),
    re_path(r'^script/([a-z_-]+)$', views.script, name='scripts'),
    re_path(r'^sources/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.SourceManifest, name='source_manifest'),
    re_path(r'^sources/(?P<pk>[a-zA-Z0-9-]+)', views.SourceDetail.as_view(), name='source_detail'),
    re_path(r'^sources/?', views.SourceMain.as_view(), name='source_main'),
    path('dt', views.DataTableProvider.as_view(), name='dt_provider'),
    re_path(r'^pages/(?P<pk>[a-zA-Z0-9-]+)', views.PageDetail.as_view(), name='page_detail'),
    re_path(r'^pages/', views.PageMain.as_view(), name='page_list'),
    re_path(r'^list/(?P<module>[a-z_-]+)(?:/(?P<type>[a-zA-Z]+))?/$', views.list, name='lists'),
    re_path(r'^form/([a-z_-]+)$', views.form, name='forms'),
    re_path(r'^show/([a-z_-]+)/([A-Za-z0-9-]+)$', views.show, name='shows'),
    re_path(r'^iiif/([a-z_-]+)$', views.iiif, name='iiifs'),
    re_path(r'^search/', include('haystack.urls'), name='haystack-search'),
    re_path(r'^$', views.index, name='dashboard'),
]
