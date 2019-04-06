"""
URL routing is handled here
"""
from django.urls import path, re_path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('uiref/', views.UIRefMain.as_view(), name='uiref'),
    path('scripts/', views.Scripts.as_view(), name='scripts'),
    re_path(r'^sources/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.SourceManifest, name='source_manifest'),
    re_path(r'^pages/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.PageManifest, name='page_manifest'),
    path('sources/<slug:pk>/', views.SourceDetail.as_view(), name='source_detail'),
    path('sources/', views.SourceMain.as_view(), name='source_main'),
    path('admin/', views.AdminMain.as_view(), name='admin_main'),
    path('images/<slug:pk>/', views.ImageDetail.as_view(), name='image_detail'),
    path('images/', views.ImageList.as_view(), name='image_list'),
    path('pages/<slug:pk>/', views.PageDetail.as_view(), name='page_detail'),
    path('pages/', views.PageList.as_view(), name='page_list'),
    path('su/', views.SessionUpdate, name='session_update'),
    path('search/', views.DefaultSearch.as_view(), name='search'),
    path('', views.Index.as_view(), name='dashboard'),
]
