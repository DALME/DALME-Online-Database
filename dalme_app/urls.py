from django.urls import path, re_path, include
from . import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.http import HttpResponse
from maintenance_mode import urls as maintenance_mode_urls

urlpatterns = [
    path('maintenance-mode/', include(maintenance_mode_urls)),
    path('accounts/login/', views.DalmeLogin.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('idp/', include('djangosaml2idp.urls', namespace='identity_provider')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^\.well-known/acme-challenge/DWY9GSDZjOsijpklS3RIAuBvZt2PThO7ameePcaIHm8/', lambda request: HttpResponse('DWY9GSDZjOsijpklS3RIAuBvZt2PThO7ameePcaIHm8.LbUmj5n5DqTPM7bapjsa-DennAErlpafYkGP-9eZzzo'), name='hello_world'),
    path('admin/', admin.site.urls),
    path('agents/', views.AgentList.as_view(), name='agent_list'),
    path('countries/', views.CountryList.as_view(), name='country_list'),
    path('download/<path:path>/', views.DownloadAttachment, name='download_attachment'),
    path('models/<model>/', views.ModelLists.as_view(), name='model_lists'),
    path('health/', views.HealthCheck, name='health'),
    path('images/', views.ImageList.as_view(), name='image_list'),
    path('images/<slug:pk>/', views.ImageDetail.as_view(), name='image_detail'),
    path('languages/', views.LanguageList.as_view(), name='language_list'),
    path('library/', views.LibraryList.as_view(), name='library_list'),
    path('locales/', views.LocaleList.as_view(), name='locale_list'),
    re_path(r'^pages/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.PageManifest, name='page_manifest'),
    path('places/', views.PlaceList.as_view(), name='place_list'),
    path('rights/', views.RightsList.as_view(), name='rights_list'),
    path('rights/<slug:pk>/', views.RightsDetail.as_view(), name='rights_detail'),
    path('search/', views.DefaultSearch.as_view(), name='search'),
    path('sets/', views.SetList.as_view(), name='set_list'),
    path('sets/<slug:pk>/', views.SetsDetail.as_view(), name='set_detail'),
    path('sets/go/<slug:pk>/', views.SetsRedirect.as_view(), name='sets_redirect'),
    path('sources/', views.SourceList.as_view(), name='source_list'),
    path('sources/<slug:pk>/', views.SourceDetail.as_view(), name='source_detail'),
    re_path(r'^sources/(?P<pk>[a-zA-Z0-9-]+)/manifest', views.SourceManifest, name='source_manifest'),
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
