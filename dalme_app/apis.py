
from django.contrib.auth.models import User, Group
from django.db.models import Q, Count, F, Prefetch
import re, requests, uuid, os, datetime, json, hashlib, ast, operator, uu, base64
from functools import reduce
from rest_framework import viewsets, status, views
from dalme_app.serializers import SourceSerializer, UserSerializer, NotificationSerializer, ProfileSerializer, ContentTypeSerializer, AttributeTypeSerializer, ContentXAttributeSerializer, ContentClassSerializer, TranscriptionSerializer, ImageSerializer, PageSerializer
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

class Pages(viewsets.ViewSet):
    """ API endpoint for managing pages """
    permission_classes = (DjangoModelPermissions,)
    queryset = Page.objects.all()

    def list(self, request, *args, **kwargs):
        #get basic parameters from Datatables Ajax request
        dt_para = get_dt_parameters(request)
        fields = ['name','dam_id','order']
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(dt_para['draw'])
        try:
            queryset = self.queryset
            if dt_para['search_string']:
                queryset = filter_on_search(queryset=queryset, search_string=dt_para['search_string'], fields=fields)
            queryset = get_ordered_queryset(queryset=queryset, dt_para=dt_para, fields=fields)
            #count the records in the queryset and add the values for "recordsTotal" and "recordsFiltered" to the return dictionary
            rec_count = queryset.count()
            data_dict['recordsTotal'] = rec_count
            data_dict['recordsFiltered'] = rec_count
            #filter the queryset for the current page
            queryset = queryset[dt_para['start']:dt_para['limit']]
            serializer = PageSerializer(queryset, many=True)
            data = serializer.data
            data_dict['data'] = data
        except Exception as e:
            data_dict['error'] = 'The following error occured while trying to fetch the data: ' + str(e)

        return Response(data_dict)

class Images(viewsets.ViewSet):
    """ API endpoint for managing DAM images """
    permission_classes = (DjangoModelPermissions,)
    queryset = rs_resource.objects.filter(resource_type=1, archive=0)
    queryset = queryset.annotate(collections=RawSQL('SELECT GROUP_CONCAT(collection.name SEPARATOR ", ") FROM collection_resource JOIN resource rs2 ON collection_resource.resource = rs2.ref JOIN collection ON collection.ref = collection_resource.collection WHERE rs2.ref = resource.ref', []))

    def list(self, request, *args, **kwargs):
        #get basic parameters from Datatables Ajax request
        dt_para = get_dt_parameters(request)
        fields = ['ref','has_image','creation_date','created_by','field12','field8','field3','field51','field79']
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(dt_para['draw'])
        try:
            queryset = self.queryset
            if dt_para['search_string']:
                queryset = filter_on_search(queryset=queryset, search_string=dt_para['search_string'], fields=fields)
            if dt_para['filters']:
                filters = dt_para['filters']
                if 'and_list' in filters:
                    queryset = queryset.filter(reduce(operator.and_, (Q(**q) for q in filters['and_list'])))
                if 'or_list' in filters:
                    queryset = queryset.filter(reduce(operator.or_, (Q(**q) for q in filters['or_list'])))
            queryset = get_ordered_queryset(queryset=queryset, dt_para=dt_para, fields=fields)
            #count the records in the queryset and add the values for "recordsTotal" and "recordsFiltered" to the return dictionary
            rec_count = queryset.count()
            data_dict['recordsTotal'] = rec_count
            data_dict['recordsFiltered'] = rec_count
            #filter the queryset for the current page
            queryset = queryset[dt_para['start']:dt_para['limit']]
            serializer = ImageSerializer(queryset, many=True)
            data = serializer.data
            data_dict['data'] = data
        except Exception as e:
            data_dict['error'] = 'The following error occured while trying to fetch the data: ' + str(e)

        return Response(data_dict)

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
        if int(data['version']) > int(object.version):
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
    """ API endpoint for managing notifications """
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

class Notifications(viewsets.ViewSet):
    """ API endpoint for managing notifications """
    permission_classes = (DjangoModelPermissions,)
    queryset = Notification.objects.all()

    def list(self, request, *args, **kwargs):
        #get basic parameters from Datatables Ajax request
        dt_para = get_dt_parameters(request)
        fields = ['code','level','type','text']
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(dt_para['draw'])
        try:
            queryset = self.queryset
            if dt_para['search_string']:
                queryset = self.filter_on_search(queryset=queryset, search_string=dt_para['search_string'], fields=fields)
            queryset = queryset.order_by(dt_para['order'])
            #count the records in the queryset and add the values for "recordsTotal" and "recordsFiltered" to the return dictionary
            rec_count = queryset.count()
            data_dict['recordsTotal'] = rec_count
            data_dict['recordsFiltered'] = rec_count
            #filter the queryset for the current page
            queryset = queryset[dt_para['start']:dt_para['limit']]
            serializer = NotificationSerializer(queryset, many=True)
            data = serializer.data
            data_dict['data'] = data
        except Exception as e:
            data_dict['error'] = 'The following error occured while trying to fetch the data: ' + str(e)

        return Response(data_dict)

    def create(self, request, format=None):
        data = request.data
        data_dict = {}
        pattern = re.compile(r'\[([a-z0-9]+)\]', re.IGNORECASE)
        for k,v in data.items():
            if k != 'action':
                key_list = pattern.findall(k)
                key_count = len(key_list)
                row_id = key_list[0]
                field = key_list[1]
                #generic code for nested data, not necessary here
                #if key_count > 2:
                #    counter = 2
                #    while counter != key_count:
                #        field = field+'.'+key_list[counter]
                #        counter = counter + 1
                #if row_id in data_dict:
                #    data_dict[row_id].append((field, v))
                #else:
                data_dict[field] = v
        #obj_dict = {}
        #for k,v in data_dict.items():
        #    obj_dict['id'] = k
        #    for i in v:
        #        obj_dict[i[0]] = i[1]

        serializer = NotificationSerializer(data=data_dict)
        if serializer.is_valid():
            new_obj = serializer.save()
            #get array with updated object
            object = Notification.objects.get(pk=new_obj.id)
            serializer = NotificationSerializer(object)
            data = serializer.data
            result = {}
            result['data'] = data

        else:
            #get error message as string
            result = serializer.errors

        return Response(result)

    def update(self, pk=None, format=None):
        data = request.data
        data_dict = {}
        pattern = re.compile(r'\[([a-z0-9]+)\]', re.IGNORECASE)
        for k,v in data.items():
            if k != 'action':
                key_list = pattern.findall(k)
                row_id = key_list[0]
                field = key_list[1]
                if row_id in data_dict:
                    data_dict[row_id].append((field, v))
                else:
                    data_dict[row_id] = [(field, v)]
        obj_dict = {}
        for k,v in data_dict.items():
            obj_dict['id'] = k
            for i in v:
                obj_dict[i[0]] = i[1]

        object = Notification.objects.get(pk=row_id)
        serializer = NotificationSerializer(object ,data=obj_dict)
        if serializer.is_valid():
            serializer.save()
            #get array with updated object
            object = Notification.objects.get(pk=row_id)
            serializer = NotificationSerializer(object)
            data = serializer.data
            result = {}
            result['data'] = data

        else:
            #get error message as string
            result = serializer.errors

        return Response(result)

    def destroy(self, pk=None, format=None):
        ids = self.kwargs.get('pk').split(',')
        q = Q()
        for i in ids:
            q |= Q(pk=i)
        try:
            Notification.objects.filter(q).delete()
            obj = Notification.objects.all()
            serializer = NotificationSerializer(obj, many=True)
            data = serializer.data
            result = {}
            result['data'] = data
        except:
            result = 'nope'
        return Response(result)

class Users(viewsets.ViewSet):
    """ API endpoint for managing users """

    permission_classes = (DjangoModelPermissions,)
    queryset = Profile.objects.all()

    def list(self, request, *args, **kwargs):
        #get basic parameters from Datatables Ajax request
        dt_para = get_dt_parameters(request)

        #get programatically: UserSerializer.Meta.fields
        fields = ['full_name','dam_user','wiki_user','wp_role', 'wp_user', 'user__last_login','user__is_superuser','user__username','user__first_name','user__last_name','user__email','user__is_staff','user__is_active','user__date_joined']
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(dt_para['draw'])
        try:
            queryset = self.queryset
            if dt_para['search_string']:
                queryset = filter_on_search(queryset=queryset, search_string=dt_para['search_string'], fields=fields)
            queryset = get_ordered_queryset(queryset=queryset, dt_para=dt_para, fields=fields)
            #count the records in the queryset and add the values for "recordsTotal" and "recordsFiltered" to the return dictionary
            rec_count = queryset.count()
            data_dict['recordsTotal'] = rec_count
            data_dict['recordsFiltered'] = rec_count
            #filter the queryset for the current page
            queryset = queryset[dt_para['start']:dt_para['limit']]
            serializer = ProfileSerializer(queryset, many=True)
            data = serializer.data
            data_dict['data'] = data
        except Exception as e:
            data_dict['error'] = 'The following error occured while trying to fetch the data: ' + str(e)

        return Response(data_dict)

    def create(self, request, format=None):
        display_fields = ['dam_usergroup', 'wp_role']
        result = {}
        data = request.data
        data_dict = {}
        user = {}
        groups = []
        wiki_groups = []
        for k,v in data.items():
            if k != 'action':
                k = json.loads('['+k[4:].replace(']','",').replace('[','"')[:-1]+']')
                k.pop(0)
                for i,f in enumerate(k):
                    if 'many-count' in f or f == '' or f.isdigit():
                        k.pop(i)
                if k != []:
                    if k[0] == 'user':
                        if len(k) > 1:
                            if k[1] == 'groups':
                                groups.append({k[2]:v})
                            else:
                                user[k[1]] = v
                    elif k[0] == 'wiki_groups':
                            wiki_groups.append({k[1]:v})
                    else:
                        if len(k) > 1:
                            data_dict[k[0]] = { k[1]:v }
                        else:
                            data_dict[k[0]] = v
            user['groups'] = groups
            data_dict['user'] = user
            data_dict['wiki_groups'] = wiki_groups

        serializer = ProfileSerializer(data=data_dict)
        if serializer.is_valid():
            #create wp user
            wp_dict = {
                'user_login': functions.get_unique_username(data_dict['user']['username'],'wp'),
                'user_pass': phpass_context.hash(data_dict['user']['password']),
                'user_nicename': data_dict['user']['username'],
                'user_email': data_dict['user']['email'],
                'user_registered': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
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
            #add id to data_dict
            data_dict['wp_user'] = wp_user.pk
            #create dam user
            dam_dict = {
                'username': functions.get_unique_username(data_dict['user']['username'], 'dam'),
                'password': str(uuid.uuid4().hex),
                'fullname': data_dict['full_name'],
                'email': data_dict['user']['email'],
                'usergroup': data_dict['dam_usergroup'],
                'approved': 1,
            }
            dam_user = rs_user(**dam_dict).save()
            dam_user = rs_user.objects.get(username=dam_dict['username'])
            del data_dict['dam_usergroup']
            #add id to data_dict
            data_dict['dam_user'] = dam_user.pk
            #create wiki user
            wiki_dict = {
                'user_name': bytes(functions.get_unique_username(data_dict['user']['username'], 'wiki'), encoding='ascii'),
                'user_real_name': bytes(data_dict['full_name'], encoding='ascii'),
                'user_password': bytes(str(uuid.uuid4().hex), encoding='ascii'),
                'user_email': bytes(data_dict['user']['email'], encoding='ascii'),
            }
            wiki_usr = wiki_user(**wiki_dict).save()
            wiki_usr = wiki_user.objects.get(user_name=wiki_dict['user_name'])
            for i in wiki_groups:
                dict = {
                    'ug_user': wiki_usr,
                    'ug_group': bytes(i, encoding='ascii')
                }
                wiki_user_groups(**dict).save()
            #add ids to data_dict
            data_dict['wiki_user'] = wiki_usr.pk
            serializer = ProfileSerializer(data=data_dict, context={'groups': groups})
            if serializer.is_valid():
                new_obj = serializer.save()
                #get array with updated object
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

    def update(self, pk=None, format=None):
        data = request.data
        data_dict = {}
        pattern = re.compile(r'\[([a-z0-9]+)\]', re.IGNORECASE)
        for k,v in data.items():
            if k != 'action':
                key_list = pattern.findall(k)
                row_id = key_list[0]
                field = key_list[1]
                if row_id in data_dict:
                    data_dict[row_id].append((field, v))
                else:
                    data_dict[row_id] = [(field, v)]
        obj_dict = {}
        for k,v in data_dict.items():
            obj_dict['id'] = k
            for i in v:
                obj_dict[i[0]] = i[1]

        object = Notification.objects.get(pk=row_id)
        serializer = NotificationSerializer(object ,data=obj_dict)
        if serializer.is_valid():
            serializer.save()
            #get array with updated object
            object = Notification.objects.get(pk=row_id)
            serializer = NotificationSerializer(object)
            data = serializer.data
            result = {}
            result['data'] = data

        else:
            #get error message as string
            result = serializer.errors

        return Response(result)

    def destroy(self, pk=None, format=None):
        ids = self.kwargs.get('pk').split(',')
        q = Q()
        for i in ids:
            q |= Q(pk=i)
        try:
            Notification.objects.filter(q).delete()
            obj = Notification.objects.all()
            serializer = NotificationSerializer(obj, many=True)
            data = serializer.data
            result = {}
            result['data'] = data
        except:
            result = 'nope'
        return Response(result)

class Sources(viewsets.ViewSet):
    """ API endpoint for managing sources """
    permission_classes = (DjangoModelPermissions,)
    queryset = Source.objects.all()

    def list(self, request, *args, **kwargs):
        try:
            type = self.request.GET['type']
        except:
            type = ''
        fields = ('id','type','name','short_name','parent_source','parent_source_id','is_inventory', 'attributes')
        if type == 'inventories':
            fields = ('id','type','name','short_name','parent_source','parent_source_id','is_inventory', 'attributes', 'no_folios')
        else:
            fields = ('id','type','name','short_name','parent_source','parent_source_id','is_inventory', 'attributes')
        #get basic parameters from Datatables Ajax request
        dt_para = get_dt_parameters(request)
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(dt_para['draw'])
        try:
            queryset = self.get_qset(type=type)
            if dt_para['search_string']:
                queryset = self.filter_on_search(queryset=queryset, search_string=dt_para['search_string'])
            queryset = self.get_ordered_queryset(queryset=queryset, dt_para=dt_para)
            #count the records in the queryset and add the values for "recordsTotal" and "recordsFiltered" to the return dictionary
            rec_count = queryset.count()
            data_dict['recordsTotal'] = rec_count
            data_dict['recordsFiltered'] = rec_count
            #filter the queryset for the current page
            queryset = queryset[dt_para['start']:dt_para['limit']]
            serializer = SourceSerializer(queryset, many=True, fields=fields)
            data = serializer.data
            data_dict['data'] = data
        except Exception as e:
            data_dict['error'] = 'The following error occured while trying to fetch the data: ' + str(e)

        return Response(data_dict)

    def retrieve(self, pk=None):
        queryset = Source.objects.all()
        source = get_object_or_404(queryset, pk=pk)
        serializer = SourceSerializer(source)
        return Response(serializer.data)

    def get_qset(self, *args, **kwargs):
        type = kwargs.get('type')
        queryset = self.queryset
        q_obj = Q()
        if type != '':
            if type == 'inventories':
                q_obj &= Q(is_inventory=True)
                queryset = queryset.filter(q_obj).annotate(no_folios=Count('pages'))

            else:
                content_types = DT_list.objects.get(short_name=type).content_types.all()
                for i in content_types:
                    q_obj |= Q(type=i.pk)
                queryset = queryset.filter(q_obj)

        return queryset

    def filter_on_search(self, *args, **kwargs):
        search_string = kwargs['search_string']
        queryset = kwargs['queryset']
        search_words = search_string.split()
        search_q = Q()
        kwsearch = False
        if search_words[0][-1:] == ':':
            try:
                search_col = search_words[0][0:-1]
                att_type = Attribute_type.objects.get(short_name=search_col)
                #local_fields = ['id','type','name','short_name','parent_source','is_inventory']
                kwsearch = True
            except:
                kwsearch = False

        if kwsearch:
            att_type_id = att_type.id
            att_dt = att_type.data_type
            search_words.pop(0)
            for word in search_words:
                search_word = Q(search_field__istartswith=word)
                search_q &= search_word

            att_type_id = att_type.id
            att_dt = att_type.data_type
            if att_dt == 'DATE':
                target_field = 'value_STR'
            else:
                target_field = 'value_'+ att_dt

            queryset = queryset.annotate(search_field=RawSQL('SELECT '+ target_field +' FROM dalme_app_attribute JOIN dalme_app_source src2 ON dalme_app_attribute.object_id = src2.id WHERE src2.id = dalme_app_source.id AND dalme_app_attribute.attribute_type = %s',[att_type_id])).filter(search_q)

        else:
            search_q = Q()
            for word in search_words:
                search_word = Q(name__icontains=word) | Q(type__name__icontains=word) | Q(parent_source__name__icontains=word) | Q(att_blob__icontains=word)
                search_q &= search_word

            queryset = queryset.annotate(att_blob=RawSQL('SELECT GROUP_CONCAT(dalme_app_attribute.value_STR SEPARATOR ",") FROM dalme_app_attribute JOIN dalme_app_source src2 ON dalme_app_attribute.object_id = src2.id WHERE src2.id = dalme_app_source.id', [])).filter(search_q)

        return queryset

    def get_ordered_queryset(self, *args, **kwargs):
        queryset = kwargs['queryset']
        dt_para = kwargs['dt_para']
        order_column_name = dt_para['order_column_name']
        order_dir = dt_para['order_dir']
        order = dt_para['order']
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

# GENERALIZED FUNCTIONS
def get_dt_parameters(request):
    para_dict = {}
    para_dict['draw'] = request.GET['draw'] #draw number - to allow DT to match requests to responses
    para_dict['start'] = int(request.GET['start']) #starting record
    length = int(request.GET['length']) #number of records to be displayed
    #calculate limit for queryset, i.e. upper number of Python range
    para_dict['limit'] = para_dict['start'] + length
    #check for filters
    if 'filters' in request.GET:
        filters = ast.literal_eval(request.GET['filters'])
    else:
        filters = None
    para_dict['filters'] = filters
    if request.GET['search[value]'] != '':
        search_string = request.GET['search[value]'] #global search value to be applied to all columns with searchable=true
    else:
        search_string = None
    para_dict['search_string'] = search_string
    order_column_idx = request.GET['order[0][column]']
    order_dir = request.GET['order[0][dir]']
    order_column_name = request.GET['columns['+order_column_idx+'][data]']
    if order_dir == 'desc':
        order = '-'+order_column_name
    else:
        order = order_column_name

    para_dict['order_dir'] = order_dir
    para_dict['order_column_name'] = order_column_name
    para_dict['order'] = order

    return para_dict

def filter_on_search(*args, **kwargs):
    search_string = kwargs['search_string']
    queryset = kwargs['queryset']
    fields = kwargs['fields']
    search_words = search_string.split()
    search_q = Q()
    for word in search_words:
        for f in fields:
            search_word = Q(**{'%s__icontains' % f: word})
            search_q |= search_word
    queryset = queryset.filter(search_q)
    return queryset

def get_ordered_queryset(*args, **kwargs):
    queryset = kwargs['queryset']
    fields = kwargs['fields']
    dt_para = kwargs['dt_para']
    order_column_name = dt_para['order_column_name']
    order_dir = dt_para['order_dir']
    order = dt_para['order']
    if order_column_name in fields:
        order = order_column_name
        if order_dir == 'desc':
            order = '-'+order
    queryset = queryset.order_by(order)
    return queryset

def get_error_array(errors, display_fields):
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
