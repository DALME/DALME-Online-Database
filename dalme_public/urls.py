from django.urls import path

from . import api


urlpatterns = [
    path('sources/', api.SourceList.as_view(), name='source_list'),
    path('sources/<uuid:pk>/', api.SourceDetail.as_view(), name='source_detail'),
    path('choices/', api.FilterChoices.as_view(), name='filter_choices'),
]
