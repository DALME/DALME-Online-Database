"""Define public API URLs for the IDA."""

from django.urls import include, re_path

from public import api

patterns = [
    re_path(r'^records/', api.RecordList.as_view(), name='record_list'),
    re_path(r'^records/<uuid:pk>/', api.RecordDetail.as_view(), name='record_detail'),
    re_path(r'^choices/', api.FilterChoices.as_view(), name='filter_choices'),
    re_path(r'^thumbnails/', api.Thumbnail.as_view(), name='thumbnails'),
]

urlpatterns = [
    re_path(r'^', include(patterns)),
]
