
from django.contrib.auth.models import User
from django.db.models import Q, Count, F, Prefetch
import re, requests, uuid, os, datetime, json, hashlib, ast, operator
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

class Pages(viewsets.ViewSet):
    """
    API endpoint for managing pages
    """
    permission_classes = (DjangoModelPermissions,)
    queryset = Page.objects.all()

    def list(self, request, *args, **kwargs):
        #get basic parameters from Datatables Ajax request
        dt_para = get_dt_parameters(request)
        fields = [
                'name',
                'dam_id',
                'order'
            ]
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(dt_para['draw'])
        try:
            queryset = self.queryset
            if dt_para['search_string']:
                queryset = self.filter_on_search(queryset=queryset, search_string=dt_para['search_string'], fields=fields)
            queryset = self.get_ordered_queryset(queryset=queryset, dt_para=dt_para, fields=fields)
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

    def filter_on_search(self, *args, **kwargs):
        search_string = kwargs['search_string']
        queryset = kwargs['queryset']
        fields = kwargs['fields']
        search_words = search_string.split()
        search_q = Q()

        if search_words[0][-1:] == ':':
            search_col = search_words[0][0:-1]
            if search_col in fields:
                search_words.pop(0)
                for word in search_words:
                    search_word = Q(**{'%s__istartswith' % search_col: word})
                    search_q &= search_word
        else:
            search_q = Q()
            for word in search_words:
                for f in fields:
                    search_word = Q(**{'%s__istartswith' % f: word})
                    search_q |= search_word

        queryset = queryset.filter(search_q)

        return queryset

    def get_ordered_queryset(self, *args, **kwargs):
        queryset = kwargs['queryset']
        dt_para = kwargs['dt_para']
        order_column_name = dt_para['order_column_name']
        order_dir = dt_para['order_dir']
        order = dt_para['order']
        queryset = queryset.order_by(order)

        return queryset

class Images(viewsets.ViewSet):
    """
    API endpoint for managing DAM images
    """
    permission_classes = (DjangoModelPermissions,)
    queryset = rs_resource.objects.filter(resource_type=1, archive=0)
    queryset = queryset.annotate(collections=RawSQL('SELECT GROUP_CONCAT(collection.name SEPARATOR ", ") FROM collection_resource JOIN resource rs2 ON collection_resource.resource = rs2.ref JOIN collection ON collection.ref = collection_resource.collection WHERE rs2.ref = resource.ref', []))

    def list(self, request, *args, **kwargs):
        #get basic parameters from Datatables Ajax request
        dt_para = get_dt_parameters(request)
        fields = [
                'ref',
                'has_image',
                'creation_date',
                'created_by',
                'field12',
                'field8',
                'field3',
                'field51',
                'field79',
            ]
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(dt_para['draw'])
        try:
            queryset = self.queryset
            if dt_para['search_string']:
                queryset = self.filter_on_search(queryset=queryset, search_string=dt_para['search_string'], fields=fields)
            if dt_para['filters']:
                filters = dt_para['filters']
                if 'and_list' in filters:
                    queryset = queryset.filter(reduce(operator.and_, (Q(**q) for q in filters['and_list'])))
                if 'or_list' in filters:
                    queryset = queryset.filter(reduce(operator.or_, (Q(**q) for q in filters['or_list'])))
            queryset = self.get_ordered_queryset(queryset=queryset, dt_para=dt_para, fields=fields)
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

    def filter_on_search(self, *args, **kwargs):
        search_string = kwargs['search_string']
        queryset = kwargs['queryset']
        fields = kwargs['fields']
        search_words = search_string.split()
        search_q = Q()

        if search_words[0][-1:] == ':':
            search_col = search_words[0][0:-1]
            if search_col in fields:
                search_words.pop(0)
                for word in search_words:
                    search_word = Q(**{'%s__istartswith' % search_col: word})
                    search_q &= search_word
        else:
            search_q = Q()
            for word in search_words:
                for f in fields:
                    search_word = Q(**{'%s__istartswith' % f: word})
                    search_q |= search_word

        queryset = queryset.filter(search_q)

        return queryset

    def get_ordered_queryset(self, *args, **kwargs):
        queryset = kwargs['queryset']
        dt_para = kwargs['dt_para']
        order_column_name = dt_para['order_column_name']
        order_dir = dt_para['order_dir']
        order = dt_para['order']
        queryset = queryset.order_by(order)

        return queryset

class Transcriptions(viewsets.ModelViewSet):
    """
    API endpoint for managing transcriptions
    """
    permission_classes = (DjangoModelPermissions,)
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer

    #def retrieve(self, request, pk=None):
    #    queryset = Transcription.objects.all()
    #    transcription = get_object_or_404(queryset, pk=pk)
    #    serializer = TranscriptionSerializer(transcription)
    #    data = serializer.data

    #    return Response(data)


class Models(viewsets.ViewSet):
    """
    API endpoint for managing notifications
    """
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
    """
    API endpoint for managing notifications
    """
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

    def filter_on_search(self, *args, **kwargs):
        search_string = kwargs['search_string']
        queryset = kwargs['queryset']
        fields = kwargs['fields']
        search_words = search_string.split()
        search_q = Q()

        if search_words[0][-1:] == ':' and search_words[0][0:-1] in fields:
            search_col = search_words[0][0:-1]
            search_words.pop(0)
            for word in search_words:
                search_word = Q(**{'%s__istartswith' % search_col: word})
                search_q &= search_word
        else:
            search_q = Q()
            for word in search_words:
                for f in fields:
                    search_word = Q(**{'%s__icontains' % f: word})
                    search_q |= search_word

        queryset = queryset.filter(search_q)

        return queryset

class Users(viewsets.ViewSet):
    """
    API endpoint for managing users
    """
    permission_classes = (DjangoModelPermissions,)
    queryset = Profile.objects.all()

    def list(self, request, *args, **kwargs):
        #get basic parameters from Datatables Ajax request
        dt_para = get_dt_parameters(request)
        profile_fields = ['full_name','dam_usergroup','dam_userid','wiki_groups','wiki_userid','wiki_username','wp_userid','wp_role','wp_avatar_url']
        user_fields = ['last_login','is_superuser','username','first_name','last_name','email','is_staff','is_active','date_joined']
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(dt_para['draw'])
        try:
            queryset = self.queryset
            if dt_para['search_string']:
                queryset = self.filter_on_search(queryset=queryset, search_string=dt_para['search_string'], profile_fields=profile_fields, user_fields=user_fields)
            queryset = self.get_ordered_queryset(queryset=queryset, dt_para=dt_para, user_fields=user_fields)
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

    def filter_on_search(self, *args, **kwargs):
        search_string = kwargs['search_string']
        queryset = kwargs['queryset']
        profile_fields = kwargs['profile_fields']
        user_fields = kwargs['user_fields']
        search_words = search_string.split()
        search_q = Q()


        if search_words[0][-1:] == ':':
            search_col = search_words[0][0:-1]
            if search_col in profile_fields:
                search_words.pop(0)
                for word in search_words:
                    search_word = Q(**{'%s__istartswith' % search_col: word})
                    search_q &= search_word

            elif search_col in user_fields:
                search_words.pop(0)
                for word in search_words:
                    field = 'user__'+search_col
                    search_word = search_word = Q(**{'%s__istartswith' % field: word})
                    search_q &= search_word

        else:
            search_q = Q()
            for word in search_words:
                for f in profile_fields:
                    search_word = Q(**{'%s__istartswith' % f: word})
                    search_q |= search_word

                for f in user_fields:
                    field = 'user__'+f
                    search_word = Q(**{'%s__istartswith' % field: word})
                    search_q |= search_word

        queryset = queryset.filter(search_q)

        return queryset

    def get_ordered_queryset(self, *args, **kwargs):
        queryset = kwargs['queryset']
        user_fields = kwargs['user_fields']
        dt_para = kwargs['dt_para']
        order_column_name = dt_para['order_column_name']
        order_dir = dt_para['order_dir']
        order = dt_para['order']
        if order_column_name in user_fields:
            order = 'user__'+order_column_name
            if order_dir == 'desc':
                order = '-'+order

        queryset = queryset.order_by(order)

        return queryset


class Sources(viewsets.ViewSet):
    """
    API endpoint for managing sources
    """
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
                content_types = Content_list.objects.get(short_name=type).content_types.all()
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

#def get_q_from_filters(filters):
#    q_objects = []
#    for f in filters:
#        qo = Q()

#    return q_objects

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
