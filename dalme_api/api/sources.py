import json
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_api.serializers import SourceSerializer, SourceOptionsSerializer
from dalme_app.models import Attribute, Attribute_type, Source
from dalme_api.access_policies import SourceAccessPolicy
from dalme_api.filters import SourceFilter
from ._common import DALMEBaseViewSet


class Sources(DALMEBaseViewSet):
    permission_classes = (SourceAccessPolicy,)
    queryset = Source.objects.all()
    serializer_class = SourceSerializer
    filterset_class = SourceFilter
    search_fields = ['type__name', 'name', 'short_name', 'owner__profile__full_name',
                     'primary_dataset__name', 'attributes__value_STR']
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

    @property
    def options_view(self):
        q_as = self.request.GET.get('as')
        return q_as == 'options'

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

    @action(detail=True, methods=['post', 'get'])
    def get_manifest(self, request, *args, **kwargs):
        source = self.get_object()
        pages = source.pages.all()
        dam_id_list = [page.dam_id for page in pages]
        if pages and dam_id_list:
            try:
                canvases = [json.loads(page.get_canvas()) for page in pages]
                result = {
                    "@context": "http://iiif.io/api/presentation/2/context.json",
                    "@id": source.get_absolute_url(),
                    "@type": "sc:Manifest",
                    "label": source.name,
                    "metadata": [],
                    "description": [{
                        "@value": f"Manifest for {source.name}",
                        "@language": "en"
                    }],
                    "license": "https://creativecommons.org/licenses/by/3.0/",
                    "attribution": "DALME",
                    "thumbnail": {
                        "@id": f"https://dam.dalme.org/loris/{dam_id_list[0]}/full/thm/0/default.jpg",
                        "@type": "dctypes:Image",
                        "height": 150,
                        "width": 56,
                        "format": "image/jpeg",
                        "service": {
                            "@context": "http://iiif.io/api/image/2/context.json",
                            "@id": f"https://dam.dalme.org/loris/{dam_id_list[0]}",
                            "profile": "http://iiif.io/api/image/2/level1.json"
                        }
                    },
                    "sequences": [
                        {
                            "@id": source.id,
                            "@type": "sc:Canvas",
                            "label": "Folios",
                            "canvases": canvases
                        }
                    ],
                    "structures": []
                }
                status = 201

            except Exception as e:
                result = {'error': str(e)}
                status = 400

        else:
            result = {'error': 'The pages in this source have no images associated in the DAM'}
            status = 400

        return Response(result, status)

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        if self.options_view:
            serializer_class = SourceOptionsSerializer
        return serializer_class

    def get_serializer(self, *args, **kwargs):
        serializer_class = super().get_serializer_class()
        fields = {
            'archives': ['id', 'type', 'name', 'short_name', 'is_private', 'no_records', 'attributes', 'sets'],
            'archival_files': ['id', 'type', 'name', 'short_name', 'parent', 'is_private', 'primary_dataset', 'owner', 'no_records', 'attributes', 'sets'],
            'records': ['id', 'type', 'name', 'short_name', 'parent', 'has_inventory', 'pages', 'sets', 'is_private', 'owner', 'no_folios', 'workflow', 'attributes', 'credits'],
            'bibliography': ['id', 'type', 'name', 'short_name', 'parent', 'is_private', 'owner', 'attributes', 'sets', 'no_records', 'primary_dataset']
        }

        if self.options_view:
            serializer_class = self.get_serializer_class()
            kwargs.setdefault('context', self.get_serializer_context())

        elif self.request.GET.get('format') == 'select':
            kwargs['fields'] = ['id', 'name']

        elif self.request.GET.get('class') is not None:
            kwargs['fields'] = fields[self.request.GET['class']]

        return serializer_class(*args, **kwargs)  # type: ignore

    def get_queryset(self, *args, **kwargs):
        if self.request.GET.get('class'):
            queryset = self.get_queryset_by_source_type()
        else:
            queryset = Source.objects.all()

        if self.options_view:
            return super().get_queryset(*args, **kwargs)
        else:
            return queryset.prefetch_related('children', 'attributes', 'sets', 'type')

    def get_queryset_by_source_type(self):
        query = {
            'archives': Q(type=19),
            'archival_files': Q(type=12),
            'records': Q(type=13),
            'bibliography': Q(type__in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
        }
        return Source.objects.filter(query[self.request.GET['class']])
