from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_app.serializers import SourceSerializer
from dalme_app.models import Attribute, Attribute_type, Source
from dalme_app.access_policies import SourceAccessPolicy
from dalme_app.filters import SourceFilter
from ._common import DALMEBaseViewSet


class Sources(DALMEBaseViewSet):
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
            result = {'message': 'Update succesful.'}
            status = 201
        except Exception as e:
            result = {'error': str(e)}
            status = 400
        return Response(result, status)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.serializer_class
        fields = {
            'archives': ['id', 'type', 'name', 'short_name', 'is_private', 'no_records', 'attributes', 'sets'],
            'archival_files': ['id', 'type', 'name', 'short_name', 'parent', 'is_private', 'primary_dataset', 'owner', 'no_records', 'attributes', 'sets'],
            'records': ['id', 'type', 'name', 'short_name', 'parent', 'has_inventory', 'pages', 'sets', 'is_private', 'owner', 'no_folios', 'workflow', 'attributes', 'credits'],
            'bibliography': ['id', 'type', 'name', 'short_name', 'parent', 'is_private', 'owner', 'attributes', 'sets']
        }
        if self.request.GET.get('class') is not None:
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
