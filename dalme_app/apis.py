from django.contrib.auth.models import User, Group
from django.db.models import Q, Count, F, Prefetch
import re, requests, uuid, os, datetime, json, hashlib, ast, operator, uu, base64
from functools import reduce
from rest_framework import viewsets, status, views
from dalme_app.serializers import *
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_app.models import *
from django.db.models.expressions import RawSQL
from django.db.models.functions import Concat
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.shortcuts import get_object_or_404
from passlib.apps import phpass_context
from dalme_app import functions
import logging
logger = logging.getLogger('DJANGO_APIS')

class DTViewSet(viewsets.ViewSet):
    """ Generic viewset for managing communication with DataTables. Should be subclassed for specific API endpoints. """
    permission_classes = (DjangoModelPermissions,)

    def list(self, request, *args, **kwargs):
        dt_data = json.loads(request.GET['data'])
        try:
            filters = ast.literal_eval(request.GET['filters'])
        except:
            filters = False
        data_dict = {}
        data_dict['draw'] = int(dt_data.get('draw')) #cast return "draw" value as INT to prevent Cross Site Scripting (XSS) attacks
        try:
            queryset = self.get_qset()
            if dt_data['search']['value']:
                queryset = self.filter_on_search(queryset=queryset, dt_data=dt_data)
            if filters:
                queryset = self.filter_on_filters(queryset=queryset, filters=filters)
            queryset = self.get_ordered_queryset(queryset=queryset, dt_data=dt_data)
            rec_count = queryset.count()
            data_dict['recordsTotal'] = rec_count
            data_dict['recordsFiltered'] = rec_count
            #filter the queryset for the current page
            queryset = queryset[dt_data.get('start'):dt_data.get('start')+dt_data.get('length')]
            serializer = self.get_serializer(queryset=queryset)
            data = serializer.data
            data_dict['data'] = data
        except Exception as e:
            data_dict['error'] = 'The following error occured while trying to fetch the data: ' + str(e)
        return Response(data_dict)

    def get_qset(self, *args, **kwargs):
        return self.queryset

    def filter_on_search(self, *args, **kwargs):
        return filter_on_search(*args, **kwargs)

    def filter_on_filters(self, *args, **kwargs):
        return filter_on_filters(*args, **kwargs)

    def get_ordered_queryset(self, *args, **kwargs):
        return get_ordered_queryset(*args, **kwargs)

    def get_serializer(self, *args, **kwargs):
        serializer = self.serializer
        queryset = kwargs['queryset']
        return serializer(queryset, many=True)

class Options(viewsets.ViewSet):
    """ API endpoint for generating lists of options for DTE forms """
    permission_classes = (DjangoModelPermissions,)
    queryset = Workset.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            form = self.request.GET['form']
            data_dict = {}
            if form == 'createtask':
                staff_options = "['Profile.objects.all()','full_name','user_id']"
                staff = functions.get_dte_options(staff_options, 'chosen')
                worksets_options = '[\'Workset.objects.filter(owner='+str(request.user.id)+')\',\'name\',\'id\']'
                worksets = functions.get_dte_options(worksets_options, 'chosen')
                groups = request.user.groups.all()
                all_lists = TaskList.objects.all()
                lists = [{'label': "", 'value': ""}]
                for list in all_lists:
                    if list.group in groups:
                        lists.append({'label': list.name+' ('+list.group+')', 'value': list.id})
                data_dict['staff'] = staff
                data_dict['worksets'] = worksets
                data_dict['lists'] = lists
            elif form == 'createtasklist':
                groups = []
                ugroups = request.user.groups.all()
                for g in ugroups:
                    groups.append({'label': g.name, 'value': g.id})
                data_dict['groups'] = groups
        except Exception as e:
            data_dict['error'] = 'The following error occured while trying to fetch the data: ' + str(e)
        return Response(data_dict)

class Worksets(viewsets.ModelViewSet):
    """ API endpoint for managing worksets """
    permission_classes = (DjangoModelPermissions,)
    queryset = Workset.objects.all()
    serializer_class = WorksetSerializer

    def create(self, request, format=None):
        data = request.data
        data_dict = {
            'name': data['data[0][name]'],
            'description': data['data[0][description]'],
            'query': data['query'],
        }
        serializer = WorksetSerializer(data=data_dict)
        if serializer.is_valid():
            new_obj = serializer.save()
            object = Workset.objects.get(pk=new_obj.id)
            serializer = WorksetSerializer(object)
            result = serializer.data
            status = 201
        else:
            result = get_error_array(serializer.errors)
            status = 400
        return Response(result, status)

class Tasks(DTViewSet):
    """ API endpoint for managing tasks """
    permission_classes = (DjangoModelPermissions,)
    queryset = Task.objects.all()
    serializer = TaskSerializer

    def get_qset(self, *args, **kwargs):
        try:
            list = self.request.GET['list']
            queryset = Task.objects.filter(task_list=list)
        except:
            queryset = Task.objects.all()
        return queryset

    def create(self, request, format=None):
        result = {}
        data_dict = get_dte_data(request)
        data_dict = data_dict[0][1]
        serializer = TaskSerializer(data=data_dict)
        if serializer.is_valid():
            new_obj = serializer.save()
            object = Task.objects.get(pk=new_obj.id)
            serializer = TaskSerializer(object)
            result['data'] = serializer.data
            status=201
        else:
            result['fieldErrors'] = get_error_array(serializer.errors)
            status=400
        return Response(result, status)

    # def update(self, request, pk=None, format=None):
    #     data = request.data
    #     object = self.get_object()
    #     serializer = TaskSerializer(object, data=data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         serializer = TaskSerializer(object)
    #         result = serializer.data
    #         status = 201
    #     else:
    #         result = serializer.errors
    #         status = 400
    #     return Response(result, status)

class TaskLists(DTViewSet):
    """ API endpoint for managing tasks lists """
    permission_classes = (DjangoModelPermissions,)
    queryset = TaskList.objects.all().annotate(task_count=Count('task'))
    serializer = TaskListSerializer

    def create(self, request, format=None):
        result = {}
        data_dict = get_dte_data(request)
        data_dict = data_dict[0][1]
        serializer = TaskListSerializer(data=data_dict)
        if serializer.is_valid():
            new_obj = serializer.save()
            object = TaskList.objects.get(pk=new_obj.id)
            serializer = TaskListSerializer(object)
            result['data'] = serializer.data
            status=201
        else:
            result['fieldErrors'] = get_error_array(serializer.errors)
            status=400
        return Response(result, status)

class Pages(DTViewSet):
    """ API endpoint for managing pages """
    permission_classes = (DjangoModelPermissions,)
    queryset = Page.objects.all()
    serializer = PageSerializer

class Images(DTViewSet):
    """ API endpoint for managing DAM images """
    permission_classes = (DjangoModelPermissions,)
    queryset = rs_resource.objects.filter(resource_type=1, archive=0)
    queryset = queryset.annotate(collections=RawSQL('SELECT GROUP_CONCAT(collection.name SEPARATOR ", ") FROM collection_resource JOIN resource rs2 ON collection_resource.resource = rs2.ref JOIN collection ON collection.ref = collection_resource.collection WHERE rs2.ref = resource.ref', []))
    serializer = ImageSerializer

    @action(detail=True)
    def get_preview_url(self, request, pk=None):
        result = {}
        try:
            url = functions.get_dam_preview(pk)
            result['preview_url'] = url
            status=201
        except Exception as e:
            result['error'] = str(e)
            status=400
        return Response(result, status)

    def retrieve(self, request, pk=None):
        image = get_object_or_404(self.queryset, pk=pk)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

class Transcriptions(viewsets.ModelViewSet):
    """ API endpoint for managing transcriptions """
    permission_classes = (DjangoModelPermissions,)
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer

    def create(self, request, format=None):
        data = request.data
        s_data = { 'version': data['version'], 'transcription': data['transcription'] }
        serializer = TranscriptionSerializer(data=s_data)
        if serializer.is_valid():
            new_obj = serializer.save()
            object = Transcription.objects.get(pk=new_obj.id)
            sp = Source_pages.objects.get(source_id=data['source'], page_id=data['page'])
            sp.transcription_id = object
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

class Models(viewsets.ViewSet):
    """ API endpoint for managing models """
    permission_classes = (DjangoModelPermissions,)
    queryset = Content_type.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            type = self.request.GET['type']
        except:
            type = ''
        try:
            subtype = self.request.GET['st']
        except:
            subtype = ''
        #get basic parameters from Datatables Ajax request
        dt_para = get_dt_parameters(request)
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(dt_para['draw'])
        try:
            queryset = self.get_qset(type=type, subtype=subtype)
            #queryset = queryset.order_by(dt_para['order'])
            #count the records in the queryset and add the values for "recordsTotal" and "recordsFiltered" to the return dictionary
            rec_count = queryset.count()
            data_dict['recordsTotal'] = rec_count
            data_dict['recordsFiltered'] = rec_count
            #filter the queryset for the current page
            queryset = queryset[dt_para['start']:dt_para['limit']]
            data_dict['data'] = self.serialize_queryset(queryset=queryset, type=type, subtype=subtype)
        except Exception as e:
            data_dict['error'] = 'The following error occured while trying to fetch the data: ' + str(e)

        return Response(data_dict)

    def get_qset(self, *args, **kwargs):
        type = kwargs['type']
        subtype = kwargs['subtype']
        if type == 'classes':
            queryset = Content_class.objects.all()

        elif type == 'content':
            if subtype == '':
                queryset = Content_type.objects.all()
            else:
                queryset = Content_type.objects.filter(content_class=subtype)

        elif type == 'attributes':
            if subtype == '':
                queryset = Attribute_type.objects.all()
            else:
                queryset = Content_attributes.objects.filter(content_type_id=subtype).order_by('order')

        return queryset

    def serialize_queryset(self, *args, **kwargs):
        queryset = kwargs['queryset']
        type = kwargs['type']
        subtype = kwargs['subtype']
        if type == 'classes':
            serializer = ContentClassSerializer(queryset, many=True)
        elif type == 'content':
            serializer = ContentTypeSerializer(queryset, many=True)
        elif type == 'attributes':
            if subtype == '':
                serializer = AttributeTypeSerializer(queryset, many=True)
            else:
                serializer = ContentXAttributeSerializer(queryset, many=True)

        data = serializer.data
        return data

# class Notifications(DTViewSet):
#     """ API endpoint for managing notifications """
#     permission_classes = (DjangoModelPermissions,)
#     queryset = Notification.objects.all()
#     serializer = NotificationSerializer
#
#     def create(self, request, format=None):
#         result = {}
#         data_dict = data_dict = get_dte_data(request)
#         serializer = NotificationSerializer(data=data_dict)
#         if serializer.is_valid():
#             new_obj = serializer.save()
#             object = Notification.objects.get(pk=new_obj.id)
#             serializer = NotificationSerializer(object)
#             result['data'] = serializer.data
#             status=201
#         else:
#             result['fieldErrors'] = get_error_array(serializer.errors, display_fields)
#             status=400
#         return Response(result, status)
#
#     def update(self, pk=None, format=None):
#         data = request.data
#         data_dict = {}
#         pattern = re.compile(r'\[([a-z0-9]+)\]', re.IGNORECASE)
#         for k,v in data.items():
#             if k != 'action':
#                 key_list = pattern.findall(k)
#                 row_id = key_list[0]
#                 field = key_list[1]
#                 if row_id in data_dict:
#                     data_dict[row_id].append((field, v))
#                 else:
#                     data_dict[row_id] = [(field, v)]
#         obj_dict = {}
#         for k,v in data_dict.items():
#             obj_dict['id'] = k
#             for i in v:
#                 obj_dict[i[0]] = i[1]
#         object = Notification.objects.get(pk=row_id)
#         serializer = NotificationSerializer(object ,data=obj_dict)
#         if serializer.is_valid():
#             serializer.save()
#             #get array with updated object
#             object = Notification.objects.get(pk=row_id)
#             serializer = NotificationSerializer(object)
#             data = serializer.data
#             result = {}
#             result['data'] = data
#         else:
#             #get error message as string
#             result = serializer.errors
#         return Response(result)
#
#     def destroy(self, pk=None, format=None):
#         ids = self.kwargs.get('pk').split(',')
#         q = Q()
#         for i in ids:
#             q |= Q(pk=i)
#         try:
#             Notification.objects.filter(q).delete()
#             obj = Notification.objects.all()
#             serializer = NotificationSerializer(obj, many=True)
#             data = serializer.data
#             result = {}
#             result['data'] = data
#         except:
#             result = 'nope'
#         return Response(result)

class Users(DTViewSet):
    """ API endpoint for managing users """
    permission_classes = (DjangoModelPermissions,)
    queryset = Profile.objects.all()
    serializer = ProfileSerializer

    def create(self, request, format=None):
        result = {}
        display_fields = ['dam_usergroup', 'wp_role']
        data_dict = get_dte_data(request)
        data_dict = self.clean_response(data_dict)
        serializer = ProfileSerializer(data=data_dict)
        if serializer.is_valid():
            #create wp user
            result = create_wp_user(data_dict)
            if result['status'] == 201:
                data_dict['wp_user'] = result['id']
            else:
                return Response(result['error'], result['status'])
            #create dam user
            result = create_dam_user(data_dict)
            if result['status'] == 201:
                data_dict['dam_user'] = result['id']
                data_dict.pop('dam_usergroup')
            else:
                return Response(result['error'], result['status'])
            #create wiki user
            result = create_wiki_user(data_dict)
            if result['status'] == 201:
                data_dict['wiki_user'] = result['id']
                data_dict.pop('wiki_groups')
            else:
                return Response(result['error'], result['status'])
            groups = [i['id'] for i in data_dict['user']['groups']]
            serializer = ProfileSerializer(data=data_dict, context={'groups': groups})
            if serializer.is_valid():
                new_obj = serializer.save()
                object = Profile.objects.get(pk=new_obj.id)
                serializer = ProfileSerializer(object)
                result['data'] = serializer.data
                status=201
            else:
                result['fieldErrors'] = get_error_array(serializer.errors, display_fields)
                status=400
        else:
            result['fieldErrors'] = get_error_array(serializer.errors, display_fields)
            status=400
        return Response(result, status)

    def update(self, request, pk=None, format=None):
        result = {}
        profile_id = self.kwargs.get('pk')
        object = Profile.objects.get(pk=profile_id)
        display_fields = ['dam_usergroup', 'wp_role']
        data_dict = get_dte_data(request)
        data_dict = self.clean_response(data_dict)
        dam_usergroup = data_dict.pop('dam_usergroup')
        wiki_groups = [ i['ug_group'] for i in data_dict.pop('wiki_groups')]
        groups = [ i['id'] for i in data_dict['user'].pop('groups')]
        wp_role = data_dict['wp_role']
        serializer = ProfileSerializer(object, data=data_dict, context={'groups': groups})
        if serializer.is_valid():
            serializer.save()
            if dam_usergroup != '':
                rs_user.objects.filter(ref=object.dam_user).update(usergroup=dam_usergroup)
            if wp_role != '':
                wp_usermeta.objects.filter(user_id=object.wp_user, meta_key='wp_capabilities').update(meta_value=wp_role)
            if wiki_groups != []:
                wiki_user_groups.objects.filter(ug_user=object.wiki_user).delete()
                for i in wiki_groups:
                    dict = {
                        'ug_user': object.wiki_user,
                        'ug_group': bytes(i, encoding='ascii')
                    }
                    wiki_user_groups(**dict).save()
            object = Profile.objects.get(pk=profile_id)
            serializer = ProfileSerializer(object)
            result['data'] = serializer.data
            status=201
        else:
            result['fieldErrors'] = get_error_array(serializer.errors, display_fields)
            status=400
        return Response(result, status)

    def destroy(self, request, pk=None, format=None):
        result = {}
        profile_id = self.kwargs.get('pk')
        object = Profile.objects.get(pk=profile_id)
        try:
            #django switch active to false
            User.objects.filter(id=object.user.pk).update(is_active=False)
            #resourcespace switch "approved" to false
            rs_user.objects.filter(ref=object.dam_user).update(approved=0)
            #wordpress change role to: -no role for this site- in meta, wp_capabilities = a:0:{}
            wp_usermeta.objects.filter(user_id=object.wp_user, meta_key='wp_capabilities').update(meta_value='a:0:{}')
            object = Profile.objects.get(pk=object.pk)
            serializer = ProfileSerializer(object)
            result['data'] = serializer.data
            status=201
        except Exception as e:
            result['error'] = 'There was a problem deleting the user: ' + str(e)
            status=400
        return Response(result, status)

    def clean_response(self, data_dict):
        data_dict = data_dict[0][1]
        try:
            data_dict['user']['is_staff'] = data_dict['user']['is_staff'][0]
        except:
            data_dict['user']['is_staff'] = 0
        try:
            data_dict['user']['is_superuser'] = data_dict['user']['is_superuser'][0]
        except:
            data_dict['user']['is_superuser'] = 0
        if 'groups-many-count' in data_dict['user']:
            data_dict['user'].pop('groups-many-count')
        if 'wiki_groups-many-count' in data_dict:
            data_dict.pop('wiki_groups-many-count')
        if 'dam_usergroup' in data_dict:
            data_dict['dam_usergroup'] = data_dict['dam_usergroup']['value']
        if 'wp_role' in data_dict:
            data_dict['wp_role'] = data_dict['wp_role']['value']
        return data_dict

class Sources(DTViewSet):
    """ API endpoint for managing sources """
    permission_classes = (DjangoModelPermissions,)
    queryset = Source.objects.all()
    serializer = SourceSerializer

    def retrieve(self, pk=None):
        queryset = Source.objects.all()
        source = get_object_or_404(queryset, pk=pk)
        serializer = SourceSerializer(source)
        return Response(serializer.data)

    def get_qset(self, *args, **kwargs):
        try:
            type = self.request.GET['type']
            queryset = self.queryset
            q_obj = Q()
            if type == 'inventories':
                q_obj &= Q(is_inventory=True)
                queryset = queryset.filter(q_obj).annotate(no_folios=Count('pages'))
            else:
                content_types = DT_list.objects.get(short_name=type).content_types.all()
                for i in content_types:
                    q_obj |= Q(type=i.pk)
                queryset = queryset.filter(q_obj)
        except:
            queryset = self.queryset
        return queryset

    def filter_on_search(self, *args, **kwargs):
        dt_data = kwargs['dt_data']
        search_string = dt_data['search']['value']
        queryset = kwargs['queryset']
        fields = get_searchable_fields(dt_data)
        search_words = search_string.split()
        search_q = Q()
        for word in search_words:
            search_word = Q(name__icontains=word) | Q(type__name__icontains=word) | Q(parent_source__name__icontains=word) | Q(att_blob__icontains=word)
            search_q &= search_word
        queryset = queryset.annotate(att_blob=RawSQL('SELECT GROUP_CONCAT(dalme_app_attribute.value_STR SEPARATOR ",") FROM dalme_app_attribute JOIN dalme_app_source src2 ON dalme_app_attribute.object_id = src2.id WHERE src2.id = dalme_app_source.id', [])).filter(search_q)
        return queryset

    def get_ordered_queryset(self, *args, **kwargs):
        queryset = kwargs['queryset']
        dt_data = kwargs['dt_data']
        order_column = dt_data['order'][0]['column']
        order_column_name = get_clean_field_name(dt_data['columns'][order_column]['data'])
        order_dir = dt_data['order'][0]['dir']
        if order_dir == 'desc':
            order = '-'+order_column_name
        else:
            order = order_column_name
        local_fields = ['id','type','name','short_name','parent_source','is_inventory', 'no_folios']
        if order_column_name not in local_fields:
            att_type = Attribute_type.objects.get(short_name=order_column_name)
            att_type_id = att_type.id
            att_dt = att_type.data_type
            if att_dt == 'DATE':
                target_field = 'value_STR'
            else:
                target_field = 'value_'+ att_dt
            queryset = queryset.annotate(ord_field=RawSQL('SELECT '+ target_field +' FROM dalme_app_attribute JOIN dalme_app_source src2 ON dalme_app_attribute.object_id = src2.id WHERE src2.id = dalme_app_source.id AND dalme_app_attribute.attribute_type = %s',[att_type_id]))
            if order_dir == 'desc':
                order = '-ord_field'
            else:
                order = 'ord_field'
        queryset = queryset.order_by(order)
        return queryset

    def get_serializer(self, *args, **kwargs):
        queryset = kwargs['queryset']
        try:
            type = self.request.GET['type']
        except:
            type = ''
        if type == 'inventories':
            return SourceSerializer(queryset, many=True)
        else:
            return SourceSerializer(queryset, many=True, fields=['no_folios'])

# GENERALIZED FUNCTIONS
def filter_on_search(*args, **kwargs):
    dt_data = kwargs['dt_data']
    search_string = dt_data['search']['value']
    queryset = kwargs['queryset']
    fields = get_searchable_fields(dt_data)
    search_words = search_string.split()
    search_q = Q()
    for word in search_words:
        for f in fields:
            search_word = Q(**{'%s__icontains' % f: word})
            search_q |= search_word
    queryset = queryset.filter(search_q)
    return queryset

def filter_on_filters(*args, **kwargs):
    queryset = kwargs['queryset']
    filters = kwargs['filters']
    if 'and_list' in filters:
         queryset = queryset.filter(reduce(operator.and_, (Q(**q) for q in filters['and_list'])))
    if 'or_list' in filters:
         queryset = queryset.filter(reduce(operator.or_, (Q(**q) for q in filters['or_list'])))
    return queryset

def get_searchable_fields(dt_data):
    fields = []
    columns = dt_data['columns']
    for c in columns:
        if c['searchable'] == True:
            fields.append(get_clean_field_name(c['data']))
    return fields

def get_ordered_queryset(*args, **kwargs):
    queryset = kwargs['queryset']
    dt_data = kwargs['dt_data']
    order_column = dt_data['order'][0]['column']
    order_column_name = get_clean_field_name(dt_data['columns'][order_column]['data'])
    order_dir = dt_data['order'][0]['dir']
    if order_dir == 'desc':
        order = '-'+order_column_name
    else:
        order = order_column_name
    queryset = queryset.order_by(order)
    return queryset

def get_clean_field_name(field):
    if '.' in field:
        field_list = field.split('.')
        if len(field_list) > 1 and field_list[-1] == 'name':
            field_list.pop(-1)
        field = '__'.join(field_list)
    return field

def get_error_array(errors, display_fields=[]):
    fieldErrors = []
    for k,v in errors.items():
        if type(v) is dict:
            for k2, v2 in v.items():
                field = k+'.'+k2
                fieldErrors.append({'name':field,'status':str(v2[0])})
        else:
            if k in display_fields:
                field = k+'.value'
            else:
                field = k
            fieldErrors.append({'name':field,'status':str(v[0])})
    return fieldErrors

def create_wp_user(data_dict):
    result = {}
    try:
        wp_dict = {
            'user_login': functions.get_unique_username(data_dict['user']['username'],'wp'),
            'user_pass': phpass_context.hash(data_dict['user']['password']),
            'user_nicename': data_dict['user']['username'],
            'user_email': data_dict['user']['email'],
            'user_registered': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'display_name': data_dict['full_name']
            }
        wp_meta_list = [
            ['nickname', data_dict['user']['username']],
            ['first_name', data_dict['user']['first_name']],
            ['last_name', data_dict['user']['last_name']],
            ['wp_capabilities', data_dict['wp_role']]
        ]
        wp_user = wp_users(**wp_dict).save()
        wp_user = wp_users.objects.get(user_login=wp_dict['user_login'])
        for i in wp_meta_list:
            dict = {
                'user_id': wp_user.pk,
                'meta_key': i[0],
                'meta_value': i[1],
                }
            wp_usermeta(**dict).save()
        result['status'] = 201
        result['id'] = wp_user.pk
    except Exception as e:
        result['status'] = 400
        result['error'] = 'Failed to create WordPress user. Error: '+str(e)
    return result

def create_dam_user(data_dict):
    result = {}
    try:
        dam_dict = {
            'username': functions.get_unique_username(data_dict['user']['username'], 'dam'),
            'password': str(uuid.uuid4()),
            'fullname': data_dict['full_name'],
            'email': data_dict['user']['email'],
            'usergroup': data_dict['dam_usergroup'],
            'approved': 1,
        }
        dam_user = rs_user(**dam_dict).save()
        dam_user = rs_user.objects.get(username=dam_dict['username'])
        result['status'] = 201
        result['id'] = dam_user.pk
    except Exception as e:
        result['status'] = 400
        result['error'] = 'Failed to create DAM user. Error: '+str(e)
    return result

def create_wiki_user(data_dict):
    result = {}
    try:
        wiki_dict = {
            'user_name': bytes(functions.get_unique_username(data_dict['user']['username'], 'wiki'), encoding='ascii'),
            'user_real_name': bytes(data_dict['full_name'], encoding='ascii'),
            'user_password': bytes(str(uuid.uuid4().hex), encoding='ascii'),
            'user_email': bytes(data_dict['user']['email'], encoding='ascii'),
        }
        wiki_usr = wiki_user(**wiki_dict).save()
        wiki_usr = wiki_user.objects.get(user_name=wiki_dict['user_name'])
        wiki_groups = data_dict['wiki_groups']
        for i in wiki_groups:
            dict = {
                'ug_user': wiki_usr,
                'ug_group': bytes(i['ug_group'], encoding='ascii')
            }
            wiki_user_groups(**dict).save()
        result['status'] = 201
        result['id'] = wiki_usr.pk
    except Exception as e:
        result['status'] = 400
        result['error'] = 'Failed to create Wiki user. Error: '+str(e)
    return result

def get_dte_data(request):
    dt_request = json.loads(request.data['data'])
    dt_request.pop('action')
    rows = dt_request['data']
    data_dict = []
    for k,v in rows.items():
        data_dict.append([k,v])
    return data_dict
