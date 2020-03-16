from django.urls import path

from . import views

app_name = 'dalme_public'
urlpatterns = [
    path('', views.PublicHome.as_view(), name='home'),
    path('collection/<int:pk>/', views.CollectionDetail.as_view(), name='collection_detail'),
    path('collection/<int:collection_pk>/set/<int:pk>', views.SetDetail.as_view(), name='set_detail'),
    path('sources/', views.SourceList.as_view(), name='source_list'),
    path('sources/<uuid:pk>/', views.SourceDetail.as_view(), name='source_detail'),
]
