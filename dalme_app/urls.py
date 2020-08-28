from django.urls import path, re_path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from rest_framework import routers
from dalme_app import apis
from dalme_app import web_apis
from maintenance_mode import urls as maintenance_mode_urls

router = routers.DefaultRouter()
router.register(r'sources', apis.Sources, basename='sources')
router.register(r'users', apis.Users, basename='users')
router.register(r'transcriptions', apis.Transcriptions, basename='transcriptions')
router.register(r'images', apis.Images, basename='images')
router.register(r'pages', apis.Pages, basename='pages')
router.register(r'tasks', apis.Tasks, basename='tasks')
router.register(r'tasklists', apis.TaskLists, basename='tasklists')
router.register(r'sets', apis.Sets, basename='sets')
router.register(r'options', apis.Options, basename='options')
router.register(r'dt_lists', apis.DTLists, basename='dt_lists')
router.register(r'dt_fields', apis.DTFields, basename='dt_fields')
router.register(r'attribute_types', apis.AttributeTypes, basename='attribute_types')
router.register(r'content_types', apis.ContentTypes, basename='content_types')
router.register(r'content_classes', apis.ContentClasses, basename='content_classes')
router.register(r'languages', apis.Languages, basename='languages')
router.register(r'async_tasks', apis.AsynchronousTasks, basename='async_tasks')
router.register(r'attributes', apis.Attributes, basename='attributes')
router.register(r'countries', apis.Countries, basename='countries')
router.register(r'locales', apis.Locales, basename='locales')
router.register(r'attachments', apis.Attachments, basename='attachments')
router.register(r'tickets', apis.Tickets, basename='tickets')
router.register(r'comments', apis.Comments, basename='comments')
router.register(r'workflow', apis.WorkflowManager, basename='workflow')
router.register(r'datasets', apis.Datasets, basename='datasets')
router.register(r'rights', apis.Rights, basename='rights')

web_router = routers.DefaultRouter()
web_router.register(r'records', web_apis.Records, basename='records')
web_router.register(r'collections', web_apis.Collections, basename='collections')

urlpatterns = [
    path('maintenance-mode/', include(maintenance_mode_urls)),
    path('api/', include((router.urls, 'dalme_app'), namespace='api_endpoint')),
    path('web-api/', include(web_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('accounts/login/', views.DalmeLogin.as_view(), name='login'),
    path('accounts/', include(('django.contrib.auth.urls', 'dalme_app'), namespace='dalme_auth')),
    path('idp/', include('djangosaml2idp.urls', namespace='identity_provider')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('django_admin/', admin.site.urls),
    re_path(r'^\.well-known/acme-challenge/DWY9GSDZjOsijpklS3RIAuBvZt2PThO7ameePcaIHm8/', lambda request: HttpResponse('DWY9GSDZjOsijpklS3RIAuBvZt2PThO7ameePcaIHm8.LbUmj5n5DqTPM7bapjsa-DennAErlpafYkGP-9eZzzo'), name='hello_world'),
    path('health/', views.HealthCheck, name='health'),
    path('search/', views.DefaultSearch.as_view(), name='search'),
    path('su/', views.SessionUpdate, name='session_update'),
    path('scripts/', views.Scripts.as_view(), name='scripts'),
    path('sets/', views.SetList.as_view(), name='set_list'),
    path('sets/<slug:pk>/', views.SetsDetail.as_view(), name='set_detail'),
    path('sets/go/<slug:pk>/', views.SetsRedirect.as_view(), name='sets_redirect'),
    path('models/<model>/', views.ModelLists.as_view(), name='model_lists'),
    path('languages/', views.LanguageList.as_view(), name='language_list'),
    path('async_tasks/', views.AsyncTaskList.as_view(), name='async_task_list'),
    path('countries/', views.CountryList.as_view(), name='country_list'),
    path('locales/', views.LocaleList.as_view(), name='locale_list'),
    path('rights/', views.RightsList.as_view(), name='rights_list'),
    path('rights/<slug:pk>/', views.RightsDetail.as_view(), name='rights_detail'),
    path('download/<path:path>/', views.DownloadAttachment, name='download_attachment'),
    re_path(r'^sources/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.SourceManifest, name='source_manifest'),
    re_path(r'^pages/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.PageManifest, name='page_manifest'),
    path('sources/', views.SourceList.as_view(), name='source_list'),
    path('sources/<slug:pk>/', views.SourceDetail.as_view(), name='source_detail'),
    path('images/', views.ImageList.as_view(), name='image_list'),
    path('images/<slug:pk>/', views.ImageDetail.as_view(), name='image_detail'),
    path('pages/', views.PageList.as_view(), name='page_list'),
    path('pages/<slug:pk>/', views.PageDetail.as_view(), name='page_detail'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<username>/', views.UserDetail.as_view(), name='user_detail'),
    path('tasks/', views.TasksList.as_view(), name='task_list'),
    path('tasks/<slug:pk>/', views.TasksDetail.as_view(), name='task_detail'),
    path('tickets/', views.TicketList.as_view(), name='ticket_list'),
    path('tickets/<slug:pk>/', views.TicketDetail.as_view(), name='ticket_detail'),
    path('', views.Index.as_view(), name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
