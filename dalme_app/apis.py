import json
import os
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordResetForm
from django.db.models import Q, Count
from django.utils import timezone
from django.http import HttpRequest
from django.conf import settings

from django_celery_results.models import TaskResult
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import FileUploadParser, FormParser, MultiPartParser

from dalme_app.serializers import (LanguageSerializer, TaskSerializer, GroupSerializer,
                                   TaskListSerializer, PageSerializer, RSImageSerializer, TranscriptionSerializer,
                                   SourceSerializer, UserSerializer, AttributeTypeSerializer, ContentXAttributeSerializer,
                                   ContentTypeSerializer, ContentClassSerializer, AsyncTaskSerializer, SimpleAttributeSerializer,
                                   CountrySerializer, LocaleSerializer, AttachmentSerializer, TicketSerializer, CommentSerializer,
                                   WorkflowSerializer, SetSerializer, RightsSerializer)
from dalme_app.models import (Attribute_type, Content_class, Content_type, Content_attributes,
                              Page, Source_pages, Source, Transcription, LanguageReference,
                              TaskList, Task, rs_resource, rs_collection, rs_collection_resource,
                              Attribute, CountryReference, LocaleReference, Attachment, Ticket,
                              Comment, Workflow, Set, Set_x_content, RightsPolicy, Work_log, get_dam_preview)
from dalme_app.access_policies import GeneralAccessPolicy, SourceAccessPolicy, SetAccessPolicy, WorkflowAccessPolicy, UserAccessPolicy
from dalme_app.filters import SourceFilter

class DTViewSet(viewsets.ModelViewSet):
    """ Generic viewset for managing communication with DataTables.
    Should be subclassed for specific API endpoints. """

    choice_keys = ['i[\'name\']', 'i[\'id\']']

    @action(detail=True, methods=['post'])
    def has_permission(self, request, pk=None):
        object = self.get_object()
        self.check_object_permissions(self.request, object)
        return Response(200)

    @action(detail=True, methods=['patch'])
    def change_owner(self, request, *args, **kwargs):
        result = {}
        object = self.get_object()
        try:
            new_owner = self.request.POST['new_owner']
            object.owner = new_owner
            object.save(update_fields=['owner', 'modification_user', 'modification_timestamp'])
            result['message'] = 'Owner changed succesfully.'
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)

    def list(self, request, *args, **kwargs):
        full_queryset = self.get_queryset()
        queryset = self.filter_queryset(full_queryset)

        if request.GET.get('data') is not None:
            dt_request = json.loads(request.GET['data'])
            page = self.paginate_queryset(queryset, dt_request.get('start'), dt_request.get('length'))
            serializer = self.get_serializer(page, many=True, context={'choice_keys': self.choice_keys})
            result = {
                'draw': int(dt_request.get('draw')),  # cast return "draw" value as INT to prevent Cross Site Scripting (XSS) attacks
                'recordsTotal': full_queryset.count(),
                'recordsFiltered': queryset.count(),
                'data': serializer.data
                }
        else:
            serializer = self.get_serializer(queryset, many=True, context={'choice_keys': self.choice_keys})
            result = serializer.data
        return Response(result)

    def paginate_queryset(self, queryset, start, length):
        if start is not None and length is not None:
            page = queryset[start:start+length]
            if page is not None:
                queryset = page
        return queryset

    def get_renderer_context(self):
        return {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None),
            'choice_keys': self.choice_keys
        }

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }


class AsynchronousTasks(DTViewSet):
    """ API endpoint for managing asynchronous tasks """
    permission_classes = (GeneralAccessPolicy,)
    queryset = TaskResult.objects.all()
    serializer_class = AsyncTaskSerializer


class Attachments(viewsets.ModelViewSet):
    """ API endpoint for managing attachments """
    permission_classes = (GeneralAccessPolicy,)
    parser_classes = (MultiPartParser, FormParser, FileUploadParser,)
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def create(self, request, format=None):
        result = {}
        try:
            new_obj = Attachment()
            new_obj.file = request.data['upload']
            new_obj.save()
            result['upload'] = {'id': new_obj.id}
            result['files'] = {'Attachment': {str(new_obj.id): {
                'filename': str(new_obj.filename),
                'web_path': str(new_obj.file)
            }}}
            status = 201
        except Exception as e:
            result['error'] = 'There was an error processing the file: '+str(e)
            status = 400
        return Response(result, status)


class Attributes(DTViewSet):
    """ API endpoint for managing attributes """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Attribute.objects.all().order_by('attribute_type')
    serializer_class = SimpleAttributeSerializer


class AttributeTypes(DTViewSet):
    """ API endpoint for managing attribute types """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Attribute_type.objects.all()
    serializer_class = AttributeTypeSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.GET.get('filter') is not None:
            filter = self.request.GET['filter'].split(',')
            filter_q = Q(**{filter[0]: filter[1]})
            queryset = Content_attributes.objects.filter(filter_q)
        else:
            queryset = Attribute_type.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.GET.get('filter') is not None and self.request.GET['filter'].split(',')[0] == 'content_type':
            serializer = ContentXAttributeSerializer
        else:
            serializer = self.serializer_class
        return serializer


class Choices(viewsets.ViewSet):
    """ API endpoint for generating value lists for choice fields in the UI """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Set.objects.none()

    def list(self, request, *args, **kwargs):
        result = {}
        type = self.request.GET.get('type')
        field = self.request.GET.get('field')
        if type is None or field is None:
            result['error'] = 'Request has no type/field information.'
            status = 400
        else:
            try:
                if type == 'list':
                    with open(os.path.join('dalme_app', 'config', 'value_lists', '_' + field + '.json'), 'r') as fp:
                        result = json.load(fp)
                    status = 201
                elif type == 'model':
                    para = field.split('.')
                    result = [{'label': label, 'value': value} for value, label in eval('{}._meta.get_field("{}").choices'.format(para[0], para[1]))]
                    status = 201
            except Exception as e:
                result['error'] = 'The following error occured while trying to fetch the data: ' + str(e)
                status = 400
        return Response(result, status)


class Configs(viewsets.ViewSet):
    """ API endpoint for retrieving configuration files """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Set.objects.none()

    def list(self, request, *args, **kwargs):
        result = []
        if self.request.GET.get('target') is None:
            result = {'error': 'Request has no target information.'}
            status = 400
        else:
            path = self.request.GET['path'].split(',') if self.request.GET.get('path') is not None else ''
            if self.request.GET.get('base') is not None:
                files = [self.request.GET['target'], 'base']
            else:
                try:
                    files = json.loads(self.request.GET['target'])
                except ValueError:
                    files = [self.request.GET['target']]
            if self.request.GET.get('buttons') is not None:
                files = [i['button'] for i in files if request.user.has_perm(i.get('permissions', 'auth.view_user'))]
            try:
                for file in files:
                    with open(os.path.join('dalme_app', 'config', *path, '_' + file + '.json'), 'r') as fp:
                        result.append(json.load(fp))
                status = 201
            except Exception as e:
                result = {'error': 'The following error occured while trying to fetch the data: ' + str(e)}
                status = 400

        return Response(result, status)


class ContentClasses(DTViewSet):
    """ API endpoint for managing content classes """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Content_class.objects.all()
    serializer_class = ContentClassSerializer


class ContentTypes(DTViewSet):
    """ API endpoint for managing content types """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Content_type.objects.all()
    serializer_class = ContentTypeSerializer


class Comments(viewsets.ModelViewSet):
    """ API endpoint for managing comments """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        if self.request.GET.get('model') is not None and self.request.GET.get('object') is not None:
            model = self.request.GET['model']
            object = self.request.GET['object']
            if type(object) is not str:
                object = str(object)
            obj_instance = eval(model+'.objects.get(pk="'+object+'")')
            queryset = obj_instance.comments.all()
        else:
            queryset = self.queryset
            # raise ValueError('A model and object must be provided to filter the comments dataset.')
        return queryset

    def create(self, request, *args, **kwargs):
        result = {}
        data = request.data
        try:
            content_object = eval(data['model']+'.objects.get(pk="'+data['object']+'")')
            new_comment = content_object.comments.create(body=data['body'])
            serializer = self.get_serializer(new_comment)
            result = serializer.data
            status = 201
        except Exception as e:
            result = str(e)
            status = 400
        return Response(result, status)


class Countries(DTViewSet):
    """ API endpoint for managing countries """
    permission_classes = (GeneralAccessPolicy,)
    queryset = CountryReference.objects.all()
    serializer_class = CountrySerializer
    choice_keys = ['i[\'name\']', 'i[\'name\']']


class Groups(DTViewSet):
    """ API endpoint for managing user groups """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_fields = ['id', 'name', 'properties__type']
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['name']
    choice_keys = ['i[\'name\']', 'i[\'id\']', 'i[\'properties\'][\'description\']']


class Images(DTViewSet):
    """ API endpoint for managing DAM images """
    permission_classes = (GeneralAccessPolicy,)
    queryset = rs_resource.objects.filter(resource_type=1, archive=0, ref__gte=0)
    serializer_class = RSImageSerializer
    search_dict = {'collections': 'collections__name'}

    @action(detail=True)
    def get_preview_url(self, request, pk=None):
        result = {}
        try:
            url = get_dam_preview(pk)
            result['preview_url'] = url
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)

    @action(detail=False)
    def get_info_for_source(self, request):
        result = {}
        if self.request.GET.get('data') is not None:
            try:
                data = self.request.GET['data']
                id_list = data.split(',')
                search_q = Q()
                for i in id_list:
                    q = Q(**{'ref': i})
                    search_q |= q
                queryset = self.queryset.filter(search_q)
                # collections_list = []
                folios = {}
                source_data = {}
                for image in queryset:
                    folios[image.ref] = image.field79
                    img_data = {i.resource_type_field.name: i.value for i in image.resource_data.all()
                                if i.resource_type_field.ref in [12, 29, 76, 77, 78, 80, 99]}
                    img_data['title'] = image.field8
                    img_data['country'] = image.field3
                    theme2 = image.collections.filter(theme2__isnull=False)
                    if theme2.exists() and 'archive' not in source_data:
                        img_data['archive'] = theme2[0].theme2
                    if 'city' not in source_data and img_data.get('archivalsource', '') != '' and ',' in img_data.get('archivalsource', ''):
                        img_data['city'] = img_data.get('archivalsource').split(',')[0]
                        img_data['archive'] = img_data.get('archivalsource').split(',')[1]
                    if 'collection_title' not in source_data and 'city' in img_data:
                        collections = image.collections.filter(theme=img_data['city']).exclude(name__icontains='images')
                        if collections.count() == 1:
                            img_data['collection_title'] = collections[0].name
                    for k, v in img_data.items():
                        if k not in source_data and v not in ['', ' ', None]:
                            source_data[k] = v
                short_archive = '<ARCHIVE>'
                short_series = '<SERIES>'
                if 'archive' in source_data:
                    archive = Source.objects.filter(name=source_data['archive'])
                    if archive.exists():
                        short_archive = archive[0].short_name
                if 'Series' in source_data:
                    short_series = ''.join([c for c in source_data['Series'] if c.isupper()])
                if 'person' in source_data:
                    src_title = 'Inventory of ' + source_data['person']
                    src_title_short = source_data['person'].split()[-1]
                elif 'collection_title' in source_data:
                    src_title = source_data['collection_title']
                    src_title_short = source_data['collection_title'].split()[-1]
                elif 'title' in source_data:
                    src_title = source_data['title']
                    src_title_short = source_data['title'].split()[-1]
                else:
                    src_title = ''
                    src_title_short = ''
                shelf_number = source_data.get('shelfnumber', '')
                source_data['name'] = '{} ({} {} {})'.format(src_title, short_archive, short_series, shelf_number)
                source_data['short_name'] = '{} {} {} ({})'.format(short_archive, short_series, shelf_number, src_title_short)
                result['data'] = {'source_fields': source_data, 'folios': folios}
                status = 201
            except Exception as e:
                result['error'] = str(e)
                status = 400
        else:
            result['error'] = 'A list of ids must be submitted with the request.'
            status = 400
        return Response(result, status)

    # def update(self, request, *args, **kwargs):
    #     result = {}
    #     partial = kwargs.pop('partial', False)
    #     object = self.get_object()
    #     data_dict = get_dte_data(request)
    #     data_dict = data_dict[0][1]
    #     collections = data_dict.pop('collections', None)
    #     serializer = self.get_serializer(object, data=data_dict, partial=partial)
    #     if serializer.is_valid():
    #         if collections is not None:
    #             if ',' in str(collections):
    #                 collections = [int(i) for i in collections.split(',')]
    #             else:
    #                 collections = [collections]
    #             current_collections = rs_collection_resource.objects.filter(resource=object.ref).values_list('collection', flat=True)
    #             add_collections = list(set(collections) - set(current_collections))
    #             remove_collections = list(set(current_collections) - set(collections))
    #             if add_collections:
    #                 for c in add_collections:
    #                     new_col = rs_collection_resource()
    #                     new_col.resource = object
    #                     new_col.collection = rs_collection.objects.get(pk=c)
    #                     new_col.save()
    #             if remove_collections:
    #                 q = Q(list=object.ref)
    #                 for c in remove_collections:
    #                     q &= Q(collection=c)
    #                     rs_collection_resource.objects.filter(q).delete()
    #         serializer.save()
    #         object = rs_resource.objects.get(pk=object.ref)
    #         serializer = self.get_serializer(object)
    #         result['data'] = serializer.data
    #         status = 201
    #     else:
    #         result['fieldErrors'] = get_error_array(serializer.errors)
    #         status = 400
    #     return Response(result, status)


class Languages(DTViewSet):
    """ API endpoint for managing languages """
    permission_classes = (GeneralAccessPolicy,)
    queryset = LanguageReference.objects.all()
    serializer_class = LanguageSerializer
    choice_keys = ['i[\'name\']', 'i[\'iso6393\']']


class Locales(DTViewSet):
    """ API endpoint for managing locales """
    permission_classes = (GeneralAccessPolicy,)
    queryset = LocaleReference.objects.all()
    serializer_class = LocaleSerializer
    choice_keys = ['i[\'name\']', 'i[\'name\']']


class Pages(DTViewSet):
    """ API endpoint for managing pages """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Page.objects.all()
    serializer_class = PageSerializer

    @action(detail=True, methods=['post', 'get'])
    def get_rights(self, request, *args, **kwargs):
        result = {}
        object = self.get_object()
        try:
            result['rights'] = object.get_rights()
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)


class Rights(DTViewSet):
    """ API endpoint for managing rights policies """
    permission_classes = (GeneralAccessPolicy,)
    queryset = RightsPolicy.objects.all()
    serializer_class = RightsSerializer
    choice_keys = ['i[\'name\'][\'name\']', '\'{{"class": "RightsPolicy", "id": "{}"}}\'.format(i[\'id\'].replace(\'-\', \'\'))']


class Sets(DTViewSet):
    """ API endpoint for managing sets """
    permission_classes = (SetAccessPolicy,)
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    choice_keys = ['i[\'name\']', 'i[\'id\']', 'i[\'detail_string\']']

    @action(detail=False, methods=['post'])
    def add_members(self, request, *args, **kwargs):
        result = {}
        try:
            members = json.loads(request.data['qset'])
            object = self.get_object()
            new_members = []
            for i in members:
                source_object = Source.objects.get(pk=i)
                if not Set_x_content.objects.filter(set_id=object.id, object_id=source_object.id).exists():
                    new_entry = Set_x_content()
                    new_entry.set_id = object
                    new_entry.content_object = source_object
                    new_members.append(new_entry)
            Set_x_content.objects.bulk_create(new_members)
            result['message'] = 'Action succesful.'
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)

    @action(detail=True, methods=['patch'])
    def remove_members(self, request, *args, **kwargs):
        result = {}
        try:
            set_id = kwargs.get('pk')
            members = json.loads(self.request.POST['members'])
            member_objects = Set_x_content.objects.filter(set_id=set_id, object_id__in=members)
            member_objects.delete()
            result['message'] = 'Action succesful.'
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)

    @action(detail=True, methods=['patch'])
    def workset_state(self, request, *args, **kwargs):
        result = {}
        try:
            action = self.request.POST['action']
            target = self.request.POST['target']
            set_id = kwargs.get('pk')
            object = Set_x_content.objects.get(set_id=set_id, object_id=target)
            if action == 'mark_done':
                mark = True
            elif action == 'mark_undone':
                mark = False
            object.workset_done = mark
            object.save(update_fields=['workset_done', 'modification_user', 'modification_timestamp'])
            result['message'] = 'Update succesful.'
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)

    # def create(self, request, format=None):
    #     result = {}
    #     data_dict = get_dte_data(request)
    #     data_dict = data_dict[0][1]
    #     if request.data.get('endpoint') is not None:
    #         data_dict['endpoint'] = request.data.get('endpoint')
    #     if request.data.get('qset') is not None:
    #         member_list = json.loads(request.data['qset'])
    #     else:
    #         member_list = None
    #     serializer = self.get_serializer(data=data_dict)
    #     if serializer.is_valid():
    #         new_set = serializer.save()
    #         set_object = Set.objects.get(pk=new_set.id)
    #         if member_list is not None:
    #             new_members = []
    #             for i in member_list:
    #                 source_object = Source.objects.get(pk=i)
    #                 new_entry = Set_x_content()
    #                 new_entry.set_id = set_object
    #                 new_entry.content_object = source_object
    #                 new_members.append(new_entry)
    #             Set_x_content.objects.bulk_create(new_members)
    #         serializer = SetSerializer(set_object)
    #         result = serializer.data
    #         status = 201
    #     else:
    #         result = get_error_array(serializer.errors)
    #         status = 400
    #     return Response(result, status)

    def get_queryset(self, *args, **kwargs):
        search_q = Q()
        if self.request.GET.get('type') is not None:
            type_q = Q(set_type=int(self.request.GET['type']))
            search_q &= type_q
        ownership_q = Q(owner=str(self.request.user.id)) | ~Q(permissions=1)
        search_q &= ownership_q
        queryset = self.queryset.filter(search_q)
        return queryset

    def get_object(self):
        if self.kwargs.get('pk') is not None:
            object = self.queryset.get(pk=self.kwargs.get('pk'))
        else:
            object = self.queryset.get(pk=self.request.data['data[0][set]'])
        return object


class Sources(DTViewSet):
    permission_classes = (SourceAccessPolicy,)
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filterset_class = SourceFilter
    search_fields = ['type__name', 'name', 'short_name', 'owner__profile__full_name', 'primary_dataset__name']
    ordering_fields = ['type', 'name', 'short_name', 'owner', 'primary_dataset']
    ordering = ['name']

    # search prepends:
    # '^' Starts-with search.
    # '=' Exact matches.
    # '@' Full-text search. (Currently only supported Django's PostgreSQL backend.)
    # '$' Regex search.

    # @action(detail=False, methods=['get'])
    # def get_set(self, request, *args, **kwargs):
    #     data_dict = {}
    #     if request.GET.get('data') is not None:
    #         dt_data = json.loads(request.GET['data'])
    #         if hasattr(self, 'search_dict'):
    #             search_dict = self.search_dict
    #         else:
    #             search_dict = {}
    #         queryset = self.get_queryset()
    #         try:
    #             if dt_data['search']['value']:
    #                 queryset = self.filter_on_search(queryset=queryset, dt_data=dt_data, search_dict=search_dict)
    #             if request.GET.get('filters') is not None:
    #                 queryset = self.filter_on_filters(queryset=queryset, filters=ast.literal_eval(request.GET['filters']))
    #             queryset = self.get_ordered_queryset(queryset=queryset, dt_data=dt_data, search_dict=search_dict)
    #             query_list = list(queryset.values_list('id', flat=True))
    #             data_dict['data'] = query_list
    #         except Exception as e:
    #             data_dict['error'] = 'The following error occured while trying to fetch the set: ' + str(e)
    #     else:
    #         data_dict['error'] = 'There was no data in the request.'
    #     return Response(data_dict)

    #     # @action(detail=True, methods=['post'])
    #     # def add_identity_phrase(self, request, *args, **kwargs):
    #     #     result = {}
    #     #     object = get_object_or_404(self.queryset, pk=kwargs.get('pk'))
    #     #     try:

    @action(detail=True, methods=['patch'])
    def change_description(self, request, *args, **kwargs):
        result = {}
        object = self.get_object()
        try:
            action = self.request.POST['action']
            desc_text = self.request.POST['description']
            desc_att_obj = Attribute_type.objects.get(pk=79)
            if action == 'update':
                att_obj = Attribute.objects.filter(object_id=object.id, attribute_type=desc_att_obj)[0]
                att_obj.value_TXT = desc_text
                att_obj.save(update_fields=['value_TXT', 'modification_user', 'modification_timestamp'])
            elif action == 'create':
                object.attributes.create(attribute_type=desc_att_obj, value_TXT=desc_text)
            result['message'] = 'Update succesful.'
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class
        if self.request.GET.get('st') is not None:
            kwargs['fields'] = ['id', 'name']
        return serializer_class(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        if self.request.GET.get('class') is not None:
            query = {
                'archives': Q(type=19),
                'archival_files': Q(type=12),
                'records': Q(type=13),
                'bibliography': Q(type__in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
            }
            queryset = Source.objects.filter(query[self.request.GET['class']])
        else:
            queryset = Source.objects.all()
        return queryset


class Tasks(DTViewSet):
    """ API endpoint for managing tasks """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    @action(detail=True, methods=['patch'])
    def set_state(self, request, *args, **kwargs):
        result = {}
        object = self.get_object()
        try:
            action = self.request.POST['action']
            if action == 'mark_done':
                object.completed = True
                object.save(update_fields=['completed', 'modification_user', 'modification_timestamp'])
            elif action == 'mark_undone':
                object.completed = False
                object.save(update_fields=['completed', 'modification_user', 'modification_timestamp'])
            result['message'] = 'Update succesful.'
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)


class TaskLists(DTViewSet):
    """ API endpoint for managing tasks lists """
    permission_classes = (GeneralAccessPolicy,)
    queryset = TaskList.objects.all().annotate(task_count=Count('task'))
    serializer_class = TaskListSerializer


class Tickets(DTViewSet):
    """ API endpoint for managing issue tickets """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(detail=True, methods=['patch'])
    def set_state(self, request, *args, **kwargs):
        result = {}
        object = self.get_object()
        try:
            action = self.request.POST['action']
            if action == 'Close':
                object.status = 1
                object.save(update_fields=['status', 'modification_user', 'modification_timestamp'])
            elif action == 'Open':
                object.status = 0
                object.save(update_fields=['status', 'modification_user', 'modification_timestamp'])
            result['username'] = self.request.user.username
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)


class Transcriptions(viewsets.ModelViewSet):
    """ API endpoint for managing transcriptions """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer

    def create(self, request, format=None):
        data = request.data
        s_data = {'version': data['version'], 'transcription': data['transcription']}
        serializer = TranscriptionSerializer(data=s_data)
        if serializer.is_valid():
            new_obj = serializer.save()
            object = Transcription.objects.get(pk=new_obj.id)
            sp = Source_pages.objects.get(source=data['source'], page=data['page'])
            sp.transcription = object
            sp.save()
            serializer = TranscriptionSerializer(object)
            result = serializer.data
            status = 201
        else:
            result = serializer.errors
            status = 400
        return Response(result, status)

    def update(self, request, pk=None, format=None):
        data = request.data
        object = self.get_object()
        if object.version:
            version = int(object.version)
        else:
            version = 0
        if int(data['version']) > version:
            serializer = TranscriptionSerializer(object, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                serializer = TranscriptionSerializer(object)
                result = serializer.data
                status = 201
            else:
                result = serializer.errors
                status = 400
        else:
            serializer = TranscriptionSerializer(object)
            result = serializer.data
            status = 201
        return Response(result, status)


class Users(DTViewSet):
    """ API endpoint for managing users """
    permission_classes = (UserAccessPolicy,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'profile__full_name', 'groups']
    search_fields = ['username', 'email', 'profile__full_name', 'first_name', 'last_name']
    ordering_fields = ['id', 'username', 'email', 'profile__full_name', 'last_login', 'date_joined', 'is_staff', 'is_active', 'is_superuser']
    ordering = ['first_name']
    choice_keys = ['i[\'profile\'][\'full_name\']', 'i[\'id\']']

    @action(detail=True, methods=['post'])
    def reset_password(self, request, *args, **kwargs):
        result = {}
        object = self.get_object().user
        try:
            form = PasswordResetForm({'email': object.email})
            assert form.is_valid()
            request = HttpRequest()
            request.META['SERVER_NAME'] = 'db.dalme.org'
            request.META['SERVER_PORT'] = '443'
            form.save(
                request=request,
                use_https=True,
                from_email=settings.DEFAULT_FROM_EMAIL,
                email_template_name='registration/password_reset_email_auto.html'
            )
            result['data'] = 'Email sent'
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)


class WorkflowManager(viewsets.ModelViewSet):
    """ API endpoint for managing the project's workflow """
    permission_classes = (WorkflowAccessPolicy,)
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer

    @action(detail=True, methods=['patch'])
    def change_state(self, request, *args, **kwargs):
        result = {}
        object = self.get_object()
        try:
            action = self.request.POST['action']
            stage_dict = dict(Workflow.PROCESSING_STAGES)
            status_dict = dict(Workflow.WORKFLOW_STATUS)
            if action == 'stage_done':
                stage = int(self.request.POST['code'])
                stage_name = stage_dict[stage]
                setattr(object, stage_name + '_done', True)
                object.last_user = request.user
                object.last_modified = timezone.now()
                object.save()
                self.update_log(object, stage_name + ': marked as done')
                next_stage = stage + 1
                result['prev_stage_name'] = stage_name
                result['mod_html'] = '<i class="far fa-history fa-fw"></i> Now | <a href="/users/' + request.user.username + '">' + request.user.profile.full_name + '</a>'
                if stage == 4:
                    result['status_html'] = '<div class="wf-manager-status tag-wf-awaiting">awaiting parsing</div>'
                else:
                    result['status_html'] = '<button class="wf-manager-status_btn tag-wf-awaiting" role="button" onclick="update_workflow(\'begin_stage\',' + str(next_stage) + ')">\
                    begin ' + stage_dict[next_stage] + '</button>'
            elif action == 'begin_stage':
                stage = int(self.request.POST['code'])
                stage_name = stage_dict[stage]
                object.stage = stage
                object.last_user = request.user
                object.last_modified = timezone.now()
                object.save()
                self.update_log(object, stage_name + ': work commenced')
                result['stage_name'] = stage_name
                result['mod_html'] = '<i class="far fa-history fa-fw"></i> Now | <a href="/users/' + request.user.username + '">' + request.user.profile.full_name + '</a>'
                result['status_html'] = '<div class="wf-manager-status tag-wf-in_progress">' + stage_name + ' in progress</div>\
                <button class="wf-manager-status_btn tag-wf-in_progress" role="button" onclick="update_workflow(\'stage_done\', ' + str(stage) + ')">\
                <i class="far fa-check-square fa-fw"></i> DONE</button>'
            elif action == 'toggle_help':
                if object.help_flag:
                    object.help_flag = False
                else:
                    object.help_flag = True
                object.last_user = request.user
                object.last_modified = timezone.now()
                object.save()
                self.update_log(object, 'help flag set to ' + str(object.help_flag))
            elif action == 'toggle_public':
                if object.is_public:
                    object.is_public = False
                else:
                    object.is_public = True
                object.last_user = request.user
                object.last_modified = timezone.now()
                object.save()
                self.update_log(object, 'public flag set to ' + str(object.is_public))
            elif action == 'change_status':
                status = int(self.request.POST['code'])
                prev_status = object.wf_status
                object.wf_status = status
                object.last_user = request.user
                object.last_modified = timezone.now()
                object.save()
                self.update_log(object, 'status changed from "' + status_dict[prev_status] + '" to "' + status_dict[status] + '"')
                status_name = status_dict[status]
                result['mod_html'] = '<i class="far fa-history fa-fw"></i> Now | <a href="/users/' + request.user.username + '">' + request.user.profile.full_name + '</a>'
                if status != 2:
                    result['status_html'] = '<div class="wf-manager-status tag-wf-' + status_name + '">' + status_name + '</div>'
                else:
                    stage = object.stage
                    stage_name = stage_dict[stage]
                    if getattr(object, stage_name + '_done'):
                        if stage == 4:
                            result['status_html'] = '<div class="wf-manager-status tag-wf-awaiting">awaiting parsing</div>'
                        else:
                            next_stage = stage + 1
                            result['status_html'] = '<button class="wf-manager-status_btn tag-wf-awaiting" role="button" onclick="update_workflow(\'begin_stage\', ' + str(next_stage) + ')">\
                            begin ' + stage_dict[next_stage] + '</button>'
                    else:
                        result['status_html'] = '<div class="wf-manager-status tag-wf-in_progress">' + stage_name + ' in progress</div>\
                        <button class="wf-manager-status_btn tag-wf-in_progress" role="button" onclick="update_workflow(\'stage_done\', ' + str(stage) + ')">\
                        <i class="far fa-check-square fa-fw"></i> DONE</button>'
            result['message'] = 'Update succesful.'
            status = 201
        except Exception as e:
            result['error'] = str(e)
            status = 400
        return Response(result, status)

    def update_log(self, source, message):
        Work_log.objects.create(source=source, event=message)
