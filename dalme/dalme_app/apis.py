
from django.contrib.auth.models import User
from django.db.models import Q, Count, F, Prefetch
import requests, uuid, os, datetime, json
from rest_framework import viewsets, status
from dalme_app.serializers import SourceSerializer, UserSerializer, NotificationSerializer, ProfileSerializer
from rest_framework.response import Response
from dalme_app.models import (Attribute_type, Attribute, Attribute_DATE, Attribute_DBR, Attribute_INT,
Attribute_STR, Attribute_TXT, Content_class, Content_type, Content_type_x_attribute_type,
Content_list, Content_list_x_content_type, Source, error_message, Profile)
from django.db.models.expressions import RawSQL
from django.db.models.functions import Concat


class Sources(viewsets.ViewSet):
    """
    API Endpoint for viewing and editing sources.
    """

    def list(self, request, *args, **kwargs):
        #get basic parameters from Datatables Ajax request
        draw = self.request.GET['draw'] #draw number - to allow DT to match requests to responses
        start = int(self.request.GET['start']) #starting record
        length = int(self.request.GET['length']) #number of records to be displayed
        if self.request.GET['search[value]'] != '':
            search_string = self.request.GET['search[value]'].lower() #global search value to be applied to all columns with searchable=true
        else:
            search_string = None
        order_column_idx = self.request.GET['order[0][column]']
        order_dir = self.request.GET['order[0][dir]']
        order_column_name = self.request.GET['columns['+order_column_idx+'][data]']
        if order_dir == 'desc':
            order_column_name = '-'+order_column_name
        #calculate limit for queryset, i.e. upper number of Python range
        limit = start + length
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(draw)
        #check if type of list is set
        if 'type' in self.request.GET:
            type = self.request.GET['type']
            list_type = Content_list.objects.get(short_name=type)
            def_headers = list_type.default_headers.split(',')
            if list_type.extra_headers:
                extra_headers = list_type.extra_headers.split(',')
            else:
                extra_headers = []

            q_obj = Q()

            if type == 'inventories':
                #get ALL HEADERS
                att_l = Content_type_x_attribute_type.objects.filter(content_type=13).select_related('attribute_type')
                #create query
                q_obj &= Q(is_inventory=True)

            else:
                #get ALL HEADERS
                content_types = Content_list_x_content_type.objects.filter(content_list=list_type.pk).select_related('content_type')
                q = Q()
                for c in content_types:
                    q |= Q(content_type=c.content_type)

                att_l = Content_type_x_attribute_type.objects.filter(q).select_related('attribute_type')
                #create query
                filters = []
                for i in content_types:
                    filters.append(i.content_type)

                for filter in filters:
                    q_obj |= Q(type=filter)

        #if list type is not set, then the request is for all sources
        else:
            def_headers = ['15']
            extra_headers = ['type']
            #get ALL HEADERS
            att_l = Content_type_x_attribute_type.objects.filter(content_type__content_class=1).select_related('attribute_type')
            #create query
            q_obj = ~Q(pk=None)

        #create attribute dictionary
        att_dict = {}
        #for a in att_l:
        #        if a.attribute_type.short_name not in att_dict:
        #            att_dict[a.attribute_type.short_name] = [a.attribute_type.name,a.attribute_type.data_type,str(a.attribute_type_id)]

        for a in att_l:
                if a.attribute_type.short_name not in att_dict:
                    att_dict[a.attribute_type.short_name] = [a.attribute_type.name,a.attribute_type.data_type,str(a.attribute_type_id)]

        extra_dict = {}
        for k,v in att_dict.items():
            extra_dict[k] = 'SELECT dalme_app_attribute_'+v[1].lower()+'.value FROM dalme_app_attribute_'+v[1].lower()+' JOIN dalme_app_attribute ON dalme_app_attribute.id = dalme_app_attribute_'+v[1].lower()+'.attribute_id_id JOIN dalme_app_source src2 ON dalme_app_attribute.content_id = src2.id WHERE src2.id = dalme_app_source.id AND dalme_app_attribute.attribute_type = '+v[2]

        #filter_on_search
        if search_string:
            search_words = search_string.split()
            if search_words[0][-1:] == ':' and search_words[0][0:-1] in att_dict:
                search_col = search_words[0][0:-1]
                search_words.pop(0)
                search_q = Q()
                for word in search_words:
                    search_word = Q(search_field__startswith=word)
                    search_q &= search_word

                target_table = 'dalme_app_attribute_'+att_dict[search_col][1].lower()
                target_field = target_table+'.value'
                target_table_index = target_table+'.attribute_id_id'
                att_type_id = att_dict[search_col][2]
                queryset = Source.objects.filter(q_obj).extra(select=extra_dict).annotate(search_field=RawSQL('SELECT '+ target_field +' FROM '+ target_table +' JOIN dalme_app_attribute ON dalme_app_attribute.id = '+ target_table_index +' JOIN dalme_app_source src2 ON dalme_app_attribute.content_id = src2.id WHERE src2.id = dalme_app_source.id AND dalme_app_attribute.attribute_type = %s', [att_type_id])).filter(search_q).order_by(order_column_name)

            else:
                search_q = Q()
                for word in search_words:
                    search_word = Q(name__icontains=word) | Q(att_blob__icontains=word)
                    if 'type' in extra_headers: search_word |= Q(type__name__icontains=word)
                    if 'parent_source' in extra_headers: search_word |= Q(parent_source__name__icontains=word)
                    search_q &= search_word

                queryset = Source.objects.filter(q_obj).extra(select=extra_dict).annotate(att_blob=RawSQL('SELECT GROUP_CONCAT(dalme_app_attribute_str.value SEPARATOR ",") FROM dalme_app_attribute_str JOIN dalme_app_attribute ON dalme_app_attribute.id = dalme_app_attribute_str.attribute_id_id JOIN dalme_app_source src2 ON dalme_app_attribute.content_id = src2.id WHERE src2.id = dalme_app_source.id', [])).filter(search_q).order_by(order_column_name)

        else:
            queryset = Source.objects.filter(q_obj).extra(select=extra_dict).order_by(order_column_name)

        #count the records in the queryset and add the values for "recordsTotal" and "recordsFiltered" to the return dictionary
        rec_count = queryset.count()
        data_dict['recordsTotal'] = rec_count
        data_dict['recordsFiltered'] = rec_count
        #filter the queryset for the current page
        queryset = queryset[start:limit]
        #create an array of fields present in the dataset. This will be used to dynamically filter the fields in the serializer
        fields = ['id','name']
        if extra_headers:
            for i in extra_headers:
                fields.append(i)

        for id, names in att_dict.items():
            fields.append(id)

        serializer = SourceSerializer(queryset, many=True, fields=fields)
        data = serializer.data
        data_dict['data'] = data

        return Response(data_dict)

class Users(viewsets.ViewSet):
    """
    API Endpoint for viewing and editing users.
    """

    def list(self, request, *args, **kwargs):
        #get basic parameters from Datatables Ajax request
        draw = self.request.GET['draw'] #draw number - to allow DT to match requests to responses
        start = int(self.request.GET['start']) #starting record
        length = int(self.request.GET['length']) #number of records to be displayed
        if self.request.GET['search[value]'] != '':
            search_string = self.request.GET['search[value]'].lower() #global search value to be applied to all columns with searchable=true
        else:
            search_string = None
        order_column_idx = self.request.GET['order[0][column]']
        order_dir = self.request.GET['order[0][dir]']
        order_column_name = self.request.GET['columns['+order_column_idx+'][data]']
        if order_dir == 'desc':
            order_column_name = '-'+order_column_name
        #calculate limit for queryset, i.e. upper number of Python range
        limit = start + length
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(draw)

        #filter_on_search
        if search_string:
            search_words = search_string.split()
            if search_words[0][-1:] == ':' and search_words[0][0:-1] in att_dict:
                search_col = search_words[0][0:-1]
                search_words.pop(0)
                search_q = Q()
                for word in search_words:
                    search_word = Q(search_field__startswith=word)
                    search_q &= search_word

                target_table = 'dalme_app_attribute_'+att_dict[search_col][1].lower()
                target_field = target_table+'.value'
                target_table_index = target_table+'.attribute_id_id'
                att_type_id = att_dict[search_col][2]
                queryset = Source.objects.filter(q_obj).extra(select=extra_dict).annotate(search_field=RawSQL('SELECT '+ target_field +' FROM '+ target_table +' JOIN dalme_app_attribute ON dalme_app_attribute.id = '+ target_table_index +' JOIN dalme_app_source src2 ON dalme_app_attribute.content_id = src2.id WHERE src2.id = dalme_app_source.id AND dalme_app_attribute.attribute_type = %s', [att_type_id])).filter(search_q).order_by(order_column_name)

            else:
                search_q = Q()
                for word in search_words:
                    search_word = Q(name__icontains=word) | Q(att_blob__icontains=word)
                    if 'type' in extra_headers: search_word |= Q(type__name__icontains=word)
                    if 'parent_source' in extra_headers: search_word |= Q(parent_source__name__icontains=word)
                    search_q &= search_word

                queryset = Source.objects.filter(q_obj).extra(select=extra_dict).annotate(att_blob=RawSQL('SELECT GROUP_CONCAT(dalme_app_attribute_str.value SEPARATOR ",") FROM dalme_app_attribute_str JOIN dalme_app_attribute ON dalme_app_attribute.id = dalme_app_attribute_str.attribute_id_id JOIN dalme_app_source src2 ON dalme_app_attribute.content_id = src2.id WHERE src2.id = dalme_app_source.id', [])).filter(search_q).order_by(order_column_name)

        else:
            queryset = Profile.objects.all().order_by(order_column_name)

        #count the records in the queryset and add the values for "recordsTotal" and "recordsFiltered" to the return dictionary
        rec_count = queryset.count()
        data_dict['recordsTotal'] = rec_count
        data_dict['recordsFiltered'] = rec_count
        #filter the queryset for the current page
        queryset = queryset[start:limit]
        serializer = ProfileSerializer(queryset, many=True)
        data = serializer.data
        data_dict['data'] = data

        return Response(data_dict)

class Notifications(viewsets.ViewSet):
    """
    API Endpoint for viewing and editing notifications and error messages.
    """

    def list(self, request, *args, **kwargs):
        #get basic parameters from Datatables Ajax request
        draw = self.request.GET['draw'] #draw number - to allow DT to match requests to responses
        start = int(self.request.GET['start']) #starting record
        length = int(self.request.GET['length']) #number of records to be displayed
        if self.request.GET['search[value]'] != '':
            search_string = self.request.GET['search[value]'].lower() #global search value to be applied to all columns with searchable=true
        else:
            search_string = None
        order_column_idx = self.request.GET['order[0][column]']
        order_dir = self.request.GET['order[0][dir]']
        order_column_name = self.request.GET['columns['+order_column_idx+'][data]']
        if order_dir == 'desc':
            order_column_name = '-'+order_column_name
        #calculate limit for queryset, i.e. upper number of Python range
        limit = start + length
        #create a dictionary that will be returned as JSON + add the "draw" return value
        #cast it as INT to prevent Cross Site Scripting (XSS) attacks
        data_dict = {}
        data_dict['draw'] = int(draw)

        #filter_on_search
        if search_string:
            search_words = search_string.split()
            if search_words[0][-1:] == ':' and search_words[0][0:-1] in att_dict:
                search_col = search_words[0][0:-1]
                search_words.pop(0)
                search_q = Q()
                for word in search_words:
                    search_word = Q(search_field__startswith=word)
                    search_q &= search_word

                target_table = 'dalme_app_attribute_'+att_dict[search_col][1].lower()
                target_field = target_table+'.value'
                target_table_index = target_table+'.attribute_id_id'
                att_type_id = att_dict[search_col][2]
                queryset = Source.objects.filter(q_obj).extra(select=extra_dict).annotate(search_field=RawSQL('SELECT '+ target_field +' FROM '+ target_table +' JOIN dalme_app_attribute ON dalme_app_attribute.id = '+ target_table_index +' JOIN dalme_app_source src2 ON dalme_app_attribute.content_id = src2.id WHERE src2.id = dalme_app_source.id AND dalme_app_attribute.attribute_type = %s', [att_type_id])).filter(search_q).order_by(order_column_name)

            else:
                search_q = Q()
                for word in search_words:
                    search_word = Q(name__icontains=word) | Q(att_blob__icontains=word)
                    if 'type' in extra_headers: search_word |= Q(type__name__icontains=word)
                    if 'parent_source' in extra_headers: search_word |= Q(parent_source__name__icontains=word)
                    search_q &= search_word

                queryset = Source.objects.filter(q_obj).extra(select=extra_dict).annotate(att_blob=RawSQL('SELECT GROUP_CONCAT(dalme_app_attribute_str.value SEPARATOR ",") FROM dalme_app_attribute_str JOIN dalme_app_attribute ON dalme_app_attribute.id = dalme_app_attribute_str.attribute_id_id JOIN dalme_app_source src2 ON dalme_app_attribute.content_id = src2.id WHERE src2.id = dalme_app_source.id', [])).filter(search_q).order_by(order_column_name)

        else:
            queryset = error_message.objects.all().order_by(order_column_name)

        #count the records in the queryset and add the values for "recordsTotal" and "recordsFiltered" to the return dictionary
        rec_count = queryset.count()
        data_dict['recordsTotal'] = rec_count
        data_dict['recordsFiltered'] = rec_count
        #filter the queryset for the current page
        queryset = queryset[start:limit]
        serializer = NotificationSerializer(queryset, many=True)
        data = serializer.data
        data_dict['data'] = data

        return Response(data_dict)
