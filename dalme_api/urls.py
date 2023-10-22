from django.urls import path, include
from rest_framework import routers
from dalme_api import api
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'agents', api.Agents, basename='agents')
router.register(r'attributes', api.Attributes, basename='attributes')
router.register(r'attribute_types', api.AttributeTypes, basename='attribute_types')
router.register(r'attachments', api.Attachments, basename='attachments')
router.register(r'choices', api.Choices, basename='choices')
router.register(r'comments', api.Comments, basename='comments')
router.register(r'configs', api.Configs, basename='configs')
router.register(r'content-classes', api.ContentClasses, basename='content_classes')
router.register(r'content-types', api.ContentTypes, basename='content_types')
router.register(r'countries', api.Countries, basename='countries')
router.register(r'datasets', api.Datasets, basename='datasets')
router.register(r'groups', api.Groups, basename='groups')
router.register(r'images', api.Images, basename='images')
router.register(r'languages', api.Languages, basename='languages')
router.register(r'library', api.Library, basename='library')
router.register(r'library-references', api.LibraryReferences, basename='library_references')
router.register(r'locales', api.Locales, basename='locales')
router.register(r'pages', api.Pages, basename='pages')
router.register(r'places', api.Places, basename='places')
router.register(r'rights', api.Rights, basename='rights')
router.register(r'session', api.Session, basename='session')
router.register(r'sets', api.Sets, basename='sets')
router.register(r'sources', api.Sources, basename='sources')
router.register(r'tasks', api.Tasks, basename='tasks')
router.register(r'tasklists', api.TaskLists, basename='tasklists')
router.register(r'tickets', api.Tickets, basename='tickets')
router.register(r'transcriptions', api.Transcriptions, basename='transcriptions')
router.register(r'users', api.Users, basename='users')
router.register(r'workflow', api.WorkflowManager, basename='workflow')


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include((router.urls, 'dalme_api'), namespace='api_endpoint')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
