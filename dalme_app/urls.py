"""
URL routing is handled here
"""
from django.urls import path, re_path, include
from django.contrib import admin
from . import views

urlpatterns = [
    re_path(r'^uiref/?', views.UIRefMain.as_view(), name='uiref_main'),
    #re_path(r'^UIref/([a-z_-]+)$', views.uiref, name='uiref'),
    re_path(r'^scripts/?', views.Scripts.as_view(), name='scripts'),
    re_path(r'^sources/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.SourceManifest, name='source_manifest'),
    re_path(r'^sources/(?P<pk>[a-zA-Z0-9-]+)', views.SourceDetail.as_view(), name='source_detail'),
    re_path(r'^sources/?', views.SourceMain.as_view(), name='source_main'),
    re_path(r'^admin/?', views.AdminMain.as_view(), name='admin_main'),
    re_path(r'^pages/(?P<pk>[a-zA-Z0-9-]+)', views.PageDetail.as_view(), name='page_detail'),
    path('pages/', views.PageMain.as_view(), name='page_list'),
    path('su/', views.SessionUpdate, name='session_update'),
    #re_path(r'^list/(?P<module>[a-z_-]+)(?:/(?P<type>[a-zA-Z]+))?/$', views.list, name='lists'),
    #re_path(r'^form/([a-z_-]+)$', views.form, name='forms'),
    #re_path(r'^show/([a-z_-]+)/([A-Za-z0-9-]+)$', views.show, name='shows'),
    #re_path(r'^iiif/([a-z_-]+)$', views.iiif, name='iiifs'),
    re_path(r'^search/', views.DefaultSearch.as_view(), name='search'),
    re_path(r'^$', views.Index.as_view(), name='dashboard'),
]
