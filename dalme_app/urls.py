from django.urls import path, re_path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from rest_framework import routers
from dalme_app import api
from maintenance_mode import urls as maintenance_mode_urls

router = routers.DefaultRouter()
router.register(r'agents', api.Agents, basename='agents')
router.register(r'async-tasks', api.AsynchronousTasks, basename='async_tasks')
router.register(r'attributes', api.Attributes, basename='attributes')
router.register(r'attribute_types', api.AttributeTypes, basename='attribute_types')
router.register(r'attachments', api.Attachments, basename='attachments')
router.register(r'choices', api.Choices, basename='choices')
router.register(r'comments', api.Comments, basename='comments')
router.register(r'configs', api.Configs, basename='configs')
router.register(r'content-classes', api.ContentClasses, basename='content_classes')
router.register(r'content-types', api.ContentTypes, basename='content_types')
router.register(r'countries', api.Countries, basename='countries')
router.register(r'groups', api.Groups, basename='groups')
router.register(r'images', api.Images, basename='images')
router.register(r'languages', api.Languages, basename='languages')
router.register(r'locales', api.Locales, basename='locales')
router.register(r'pages', api.Pages, basename='pages')
router.register(r'rights', api.Rights, basename='rights')
router.register(r'sets', api.Sets, basename='sets')
router.register(r'sources', api.Sources, basename='sources')
router.register(r'tasks', api.Tasks, basename='tasks')
router.register(r'tasklists', api.TaskLists, basename='tasklists')
router.register(r'tickets', api.Tickets, basename='tickets')
router.register(r'transcriptions', api.Transcriptions, basename='transcriptions')
router.register(r'users', api.Users, basename='users')
router.register(r'workflow', api.WorkflowManager, basename='workflow')

urlpatterns = [
    path('maintenance-mode/', include(maintenance_mode_urls)),
    path('accounts/login/', views.DalmeLogin.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/', include((router.urls, 'dalme_app'), namespace='api_endpoint')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('idp/', include('djangosaml2idp.urls', namespace='identity_provider')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^\.well-known/acme-challenge/DWY9GSDZjOsijpklS3RIAuBvZt2PThO7ameePcaIHm8/', lambda request: HttpResponse('DWY9GSDZjOsijpklS3RIAuBvZt2PThO7ameePcaIHm8.LbUmj5n5DqTPM7bapjsa-DennAErlpafYkGP-9eZzzo'), name='hello_world'),
    path('admin/', admin.site.urls),
    path('agents/', views.AgentList.as_view(), name='agent_list'),
    path('async-tasks/', views.AsyncTaskList.as_view(), name='async_task_list'),
    path('countries/', views.CountryList.as_view(), name='country_list'),
    path('download/<path:path>/', views.DownloadAttachment, name='download_attachment'),
    path('models/<model>/', views.ModelLists.as_view(), name='model_lists'),
    path('health/', views.HealthCheck, name='health'),
    path('images/', views.ImageList.as_view(), name='image_list'),
    path('images/<slug:pk>/', views.ImageDetail.as_view(), name='image_detail'),
    path('languages/', views.LanguageList.as_view(), name='language_list'),
    path('locales/', views.LocaleList.as_view(), name='locale_list'),
    re_path(r'^pages/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.PageManifest, name='page_manifest'),
    path('rights/', views.RightsList.as_view(), name='rights_list'),
    path('rights/<slug:pk>/', views.RightsDetail.as_view(), name='rights_detail'),
    path('search/', views.DefaultSearch.as_view(), name='search'),
    path('sets/', views.SetList.as_view(), name='set_list'),
    path('sets/<slug:pk>/', views.SetsDetail.as_view(), name='set_detail'),
    path('sets/go/<slug:pk>/', views.SetsRedirect.as_view(), name='sets_redirect'),
    path('sources/', views.SourceList.as_view(), name='source_list'),
    path('sources/<slug:pk>/', views.SourceDetail.as_view(), name='source_detail'),
    re_path(r'^sources/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.SourceManifest, name='source_manifest'),
    path('su/', views.SessionUpdate, name='session_update'),
    path('tasks/', views.TasksList.as_view(), name='task_list'),
    path('tasks/<slug:pk>/', views.TasksDetail.as_view(), name='task_detail'),
    path('tickets/', views.TicketList.as_view(), name='ticket_list'),
    path('tickets/<slug:pk>/', views.TicketDetail.as_view(), name='ticket_detail'),
    path('tools/scripts/', views.Scripts.as_view(), name='scripts'),
    path('tools/config-editor/', views.ConfigEditor.as_view(), name='config_editor'),
    path('tools/settings/', views.Settings.as_view(), name='settings'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('users/<username>/', views.UserDetail.as_view(), name='user_detail'),
    path('', views.Index.as_view(), name='dashboard'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
