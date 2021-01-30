from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_api.serializers import SourceSerializer
from dalme_app.models import Attribute, Attribute_type, Source
from dalme_api.access_policies import SourceAccessPolicy
from dalme_api.filters import SourceFilter
from ._common import DALMEBaseViewSet


class Sources(DALMEBaseViewSet):
    permission_classes = (SourceAccessPolicy,)
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filterset_class = SourceFilter
    search_fields = ['type__name', 'name', 'short_name', 'owner__profile__full_name', 'primary_dataset__name', 'attributes__value_STR']
    ordering_fields = ['name', 'short_name', 'owner', 'primary_dataset', 'no_records', 'is_private', 'attributes.authority',
                       'attributes.format', 'attributes.locale', 'attributes.country', 'attributes.default_rights',
                       'attributes.archival_series', 'attributes.archival_number', 'attributes.date', 'attributes.start_date',
                       'attributes.end_date', 'attributes.support', 'attributes.named_persons', 'attributes.description']
    ordering_aggregates = {
        'no_records': {
            'function': 'Count',
            'expression': 'children'
        },
        'no_folios': {
            'function': 'Count',
            'expression': 'pages'
        }
    }
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
        object = self.get_object()
        if self.request.data.get('description') is not None:
            try:
                desc_text = self.request.data['description']
                desc_att_obj = Attribute_type.objects.get(pk=79)
                if Attribute.objects.filter(object_id=object.id, attribute_type=desc_att_obj).exists():
                    att_obj = Attribute.objects.get(object_id=object.id, attribute_type=desc_att_obj)
                    att_obj.value_TXT = desc_text
                    att_obj.save(update_fields=['value_TXT', 'modification_user', 'modification_timestamp'])
                else:
                    att_obj = object.attributes.create(attribute_type=desc_att_obj, value_TXT=desc_text)
                result = {'description': att_obj.value_TXT}
                status = 201
            except Exception as e:
                result = {'error': str(e)}
                status = 400
        else:
            result = {'error': 'No description supplied.'}
            status = 400
        return Response(result, status)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class
        fields = {
            'archives': ['id', 'type', 'name', 'short_name', 'is_private', 'no_records', 'attributes', 'sets'],
            'archival_files': ['id', 'type', 'name', 'short_name', 'parent', 'is_private', 'primary_dataset', 'owner', 'no_records', 'attributes', 'sets'],
            'records': ['id', 'type', 'name', 'short_name', 'parent', 'has_inventory', 'pages', 'sets', 'is_private', 'owner', 'no_folios', 'workflow', 'attributes', 'credits'],
            'bibliography': ['id', 'type', 'name', 'short_name', 'parent', 'is_private', 'owner', 'attributes', 'sets', 'no_records', 'primary_dataset']
        }

        if self.request.GET.get('format') == 'select':
            kwargs['fields'] = ['id', 'name']
        elif self.request.GET.get('class') is not None:
            kwargs['fields'] = fields[self.request.GET['class']]

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
