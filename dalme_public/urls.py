from django.urls import path, include
from . import api
from django.conf import settings
from django.conf.urls.static import static
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls


urlpatterns = [
    path('api/public/sources/', api.SourceList.as_view(), name='source_list'),
    path('api/public/sources/<uuid:pk>/', api.SourceDetail.as_view(), name='source_detail'),
    path('api/public/choices/', api.FilterChoices.as_view(), name='filter_choices'),
    path('api/public/thumbnails/', api.Thumbnail.as_view(), name='thumbnails'),
    path('cms/', include(wagtailadmin_urls)),
    path('', include(wagtail_urls)),
    path('documents/', include(wagtaildocs_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
