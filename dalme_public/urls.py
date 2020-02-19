from django.urls import path

from . import views

app_name = 'dalme_public'
urlpatterns = [
    path('sources/<uuid:pk>/', views.SourceDetail.as_view(), name='source_detail'),
]
