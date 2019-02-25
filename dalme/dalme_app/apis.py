
from django.contrib.auth.models import User
from django.db.models import Q, Count, F, Prefetch
import requests, uuid, os, datetime, json
from rest_framework import viewsets, status
from dalme_app.serializers import SourceSerializer
from rest_framework.response import Response
from dalme_app.models import (Attribute_type, Attribute, Attribute_DATE, Attribute_DBR, Attribute_INT,
Attribute_STR, Attribute_TXT, Content_class, Content_type, Content_type_x_attribute_type,
Content_list, Content_list_x_content_type, Source)
from django.db.models.expressions import RawSQL



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
                att_dict = {}
                for a in att_l:
                    if str(a.attribute_type_id) not in att_dict:
                        att_dict[str(a.attribute_type_id)] = [a.attribute_type.name,a.attribute_type.short_name,a.attribute_type.data_type]

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
                        att_dict[str(a.attribute_type_id)] = [a.attribute_type.name,a.attribute_type.short_name,a.attribute_type.data_type]
                #create query
                filters = []
                for i in content_types:
                    filters.append(i.content_type)

                for filter in filters:
                    q_obj |= Q(type=filter)

            extra_dict = {}
            for k,v in att_dict.items():
                extra_dict[v[1]] = 'SELECT dalme_app_attribute_'+v[2].lower()+'.value FROM dalme_app_attribute_'+v[2].lower()+' JOIN dalme_app_attribute ON dalme_app_attribute.id = dalme_app_attribute_'+v[2].lower()+'.attribute_id_id JOIN dalme_app_source src2 ON dalme_app_attribute.content_id = src2.id WHERE src2.id = dalme_app_source.id AND dalme_app_attribute.attribute_type = '+k

            queryset = Source.objects.filter(q_obj).extra(select=extra_dict).order_by(order_column_name)

        #if list type is not set, then the request is for all sources
        else:
            def_headers = ['15']
            extra_headers = ['type']
            #get ALL HEADERS
            att_l = Content_type_x_attribute_type.objects.filter(content_type__content_class=1).select_related('attribute_type')
            att_dict = {}
            for a in att_l:
                if str(a.attribute_type_id) not in att_dict:
                    att_dict[str(a.attribute_type_id)] = [a.attribute_type.name,a.attribute_type.short_name,a.attribute_type.data_type]

            extra_dict = {}
            for k,v in att_dict.items():
                extra_dict[v[1]] = 'SELECT dalme_app_attribute_'+v[2].lower()+'.value FROM dalme_app_attribute_'+v[2].lower()+' JOIN dalme_app_attribute ON dalme_app_attribute.id = dalme_app_attribute_'+v[2].lower()+'.attribute_id_id JOIN dalme_app_source src2 ON dalme_app_attribute.content_id = src2.id WHERE src2.id = dalme_app_source.id AND dalme_app_attribute.attribute_type = '+k

            queryset = Source.objects.all().extra(select=extra_dict).order_by(order_column_name)


        #if search_string:
        #    source_fields = ['name', 'type', 'parent_source', 'is_inventory']
        #    search_filters = Q(name__startswith=search_string) | Q(attributes__language__startswith=search_string)
            #for k,v in att_dict.items():
                #if v[1] in source_fields:
                #search_filters[v[1]] = search_string
                #else:
        #    queryset = queryset.filter(search_filters).order_by(order_column_name)

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
            fields.append(names[1])

        serializer = SourceSerializer(queryset, many=True, fields=fields)
        data = serializer.data
        data_dict['data'] = data

        return Response(data_dict)

        def q_for_search_word(self, word):
            """
            Given a word from the search text, return the Q object which you can filter on,
            to show only objects containing this word.
            Extend this in subclasses to include class-specific fields, if needed.
            """
            return Q(name=word) | Q(language=word)

        def q_for_search(self, search):
            """
            Given the text from the search box, search on each word in this text.
            Return a Q object which you can filter on, to show only those objects with _all_ the words present.
            Do not expect to override/extend this in subclasses.
            """
            q = Q()
            if search:
                searches = search.split()
                for word in searches:
                    q = q & self.q_for_search_word(word)
            return q

        def filter_on_search(self, search):
            """
            Return the objects containing the search terms.
            Do not expect to override/extend this in subclasses.
            """
            return self.filter(self.q_for_search(search))
