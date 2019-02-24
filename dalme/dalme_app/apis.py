
from django.contrib.auth.models import User
from django.db.models import Q, Count, F, Prefetch
import requests, uuid, os, datetime, json
from rest_framework import viewsets, status
from dalme_app.serializers import SourceSerializer
from  rest_framework.response import Response
from dalme_app.models import (Attribute_type, Attribute, Attribute_DATE, Attribute_DBR, Attribute_INT,
Attribute_STR, Attribute_TXT, Content_class, Content_type, Content_type_x_attribute_type,
Content_list, Content_list_x_content_type, Source)


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
            search_string = self.request.GET['search[value]'] #global search value to be applied to all columns with searchable=true
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
                att_dict = {}
                for a in att_l:
                    if str(a.attribute_type_id) not in att_dict:
                        att_dict[str(a.attribute_type_id)] = [a.attribute_type.name,a.attribute_type.short_name]

                #create query
                q_obj &= Q(is_inventory=True)

            else:
                #get ALL HEADERS
                content_types = Content_list_x_content_type.objects.filter(content_list=list_type.pk).select_related('content_type')
                q = Q()
                for c in content_types:
                    q |= Q(content_type=c.content_type)

                att_l = Content_type_x_attribute_type.objects.filter(q).select_related('attribute_type')
                att_dict = {}
                for a in att_l:
                    if str(a.attribute_type_id) not in att_dict:
                        att_dict[str(a.attribute_type_id)] = [a.attribute_type.name,a.attribute_type.short_name]
                #create query
                filters = []
                for i in content_types:
                    filters.append(i.content_type)

                for filter in filters:
                    q_obj |= Q(type=filter)

            if order_column_name != 'name':
                order_column_name = 'attributes__value'

            queryset = Source.objects.filter(q_obj).prefetch_related(Prefetch('attributes', queryset=Attribute.objects.select_related('attribute_str','attribute_type', 'attribute_date', 'attribute_dbr', 'attribute_int')), 'parent_source', 'type').order_by(order_column_name)
            
        #if list type is not set, then the request is for all sources
        else:
            def_headers = ['15']
            extra_headers = ['type']
            #get ALL HEADERS
            att_l = Content_type_x_attribute_type.objects.filter(content_type__content_class=1).select_related('attribute_type')
            att_dict = {}
            for a in att_l:
                if str(a.attribute_type_id) not in att_dict:
                    att_dict[str(a.attribute_type_id)] = [a.attribute_type.name,a.attribute_type.short_name]

            queryset = Source.objects.all().prefetch_related(Prefetch('attributes', queryset=Attribute.objects.select_related('attribute_str','attribute_type', 'attribute_date', 'attribute_dbr', 'attribute_int')), 'parent_source', 'type').order_by(order_column_name)
        #count the records in the queryset and add the values for "recordsTotal" and "recordsFiltered" to the return dictionary
        rec_count = queryset.count()
        data_dict['recordsTotal'] = rec_count
        data_dict['recordsFiltered'] = rec_count
        #filter the queryset for the current page
        queryset = queryset[start:limit]
        #create an array of fields present in the dataset. This will be used to dynamically filter the fields in the serializer
        fields = ['name']
        if extra_headers:
            for i in extra_headers:
                fields.append(i)

        for id, names in att_dict.items():
            fields.append(names[1])
        #create the return dataset by parsing the queryset
        qs = []
        for obj in queryset:
            name = {'name': obj.name,'url': obj.get_absolute_url()}
            row_dict = {'name':name}
            if 'type' in extra_headers:
                row_dict['type'] = str(obj.type)
            if 'parent_source' in extra_headers:
                row_dict['parent_source'] = str(obj.parent_source)
            if 'is_inventory' in extra_headers:
                row_dict['is_inventory'] = str(obj.is_inventory)

            all_attributes = obj.attributes.all()
            a_dic = {}
            for a in all_attributes:
                a_dic[str(a.attribute_type)] = a

            for k, v in att_dict.items():
                if v[0] in a_dic:
                    row_dict[v[1]] = str(a_dic[v[0]])
                else:
                    row_dict[v[1]] = None

            qs.append(row_dict)
        #serialize the dataset and add it to the return dictionary
        serializer = SourceSerializer(qs, many=True, fields=fields)
        data = serializer.data
        data_dict['data'] = data

        return Response(data_dict)
