import json
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_app.serializers import RSImageSerializer
from dalme_app.models import rs_resource, rs_api_query, Source
from dalme_app.access_policies import ImageAccessPolicy
from ._common import DALMEBaseViewSet
from json import JSONDecodeError


class Images(DALMEBaseViewSet):
    """ API endpoint for managing DAM images """
    permission_classes = (ImageAccessPolicy,)
    queryset = rs_resource.objects.filter(resource_type=1, archive=0, ref__gte=0)
    serializer_class = RSImageSerializer

    filterset_fields = ['ref', 'title', 'resource_type', 'country', 'field12', 'field8', 'field3', 'field51', 'field79', 'collections']
    search_fields = ['ref', 'title', 'country', 'field12', 'field8', 'field3', 'field51', 'field79']
    ordering_fields = ['ref', 'title', 'country', 'field12', 'field8', 'field3', 'field51', 'field79']
    ordering = ['ref']

    search_dict = {'collections': 'collections__name'}

    @action(detail=False)
    def rs_api(self, request, *args, **kwargs):
        correlation = {
            'q': 'param1',
            'n': 'param5',
            'size': 'param8'
            }
        try:
            query_params = {}

            for k, v in correlation.items():
                if self.request.GET.get(k) is not None:
                    query_params[v] = self.request.GET.get(k)

            # row_cutoff = query_params.get('param5', '20')  # this is to deal with a bug/feature in the RS API that returns 0s for records exceeding the row count requested
            response = rs_api_query(**query_params)
            try:
                result = json.loads(response.text) # [:int(row_cutoff)]
                status = 201
            except JSONDecodeError:
                result = 'Your search did not return any results.'
                status = 201

        except Exception as e:
            result = {'error': 'The following error occured while trying to fetch the data: ' + str(e)}
            status = 400

        return Response(result, status)

    def list(self, request, *args, **kwargs):
        query_params = {}
        if request.GET.get('search') is not None:
            query_params['param1'] = request.GET['search']
        if request.GET.get('data') is not None:
            dt_request = json.loads(request.GET['data'])
            # query_params['param5'] = dt_request['length']
        try:
            response = rs_api_query(**query_params)
            try:
                queryset = json.loads(response.text)
                if request.GET.get('data') is not None:
                    page = queryset[dt_request.get('start'):(dt_request.get('start') + dt_request.get('length'))]
                    result = {
                        'draw': int(dt_request.get('draw')),  # cast return "draw" value as INT to prevent Cross Site Scripting (XSS) attacks
                        'recordsTotal': len(queryset),
                        'recordsFiltered': len(queryset),
                        'data': page
                        }
                else:
                    result = queryset[:25]
                    status = 200
            except JSONDecodeError:
                result = 'Your search did not return any results.'
                status = 201
        except Exception as e:
            result = {'error': 'The following error occured while trying to fetch the data: ' + str(e)}
            status = 400
        return Response(result, status)

    @action(detail=False)
    def get_info_for_source(self, request):
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
                result = {'data': {'source_fields': source_data, 'folios': folios}}
                status = 201
            except Exception as e:
                result = {'error': str(e)}
                status = 400
        else:
            result = {'error': 'A list of ids must be submitted with the request.'}
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
