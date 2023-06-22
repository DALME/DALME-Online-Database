import json

from rest_framework.decorators import action
from rest_framework.response import Response

from dalme_api.access_policies import CollectionAccessPolicy
from dalme_api.filters import CollectionFilter, RecordFilter
from dalme_api.serializers import CollectionSerializer, RecordSerializer
from dalme_app.models import Collection, CollectionMembership, Record

from .base_viewset import DALMEBaseViewSet


class Collections(DALMEBaseViewSet):
    """API endpoint for managing collections."""

    permission_classes = (CollectionAccessPolicy,)
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filterset_class = CollectionFilter
    filterset_fields = [
        'id',
        'name',
        'use_as_workset',
        'is_published',
        'owner',
        'owner__profile__full_name',
    ]
    search_fields = ['name', 'owner__profile__full_name']
    ordering_fields = ['name', 'is_published', 'owner', 'owner__first_name', 'member_count']
    ordering_aggregates = {
        'member_count': {
            'function': 'Count',
            'expression': 'members',
        },
    }
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def members(self, request, *args, **kwargs):  # noqa: ARG002
        """Return collection members."""
        self.filterset_class = RecordFilter
        self.search_fields = ['id', 'name']
        self.ordering_fields = [*self.search_fields]
        obj = self.get_object()

        qs = Record.objects.filter(
            pk__in=[x.content_object.pk for x in obj.members.all().prefetch_related('content_object')],
        )
        qs = self.filter_queryset(qs)
        payload = {'count': qs.count()}

        data = self.request.GET.get('data')
        if data is not None:
            data = json.loads(data)
            qs = self.paginate_queryset(qs, data.get('start'), data.get('length'))

        serializer = RecordSerializer(qs, many=True, field_set='collection_member')
        payload['data'] = serializer.data

        return Response(payload, 201)

    @action(detail=False, methods=['post'])
    def add_members(self, request, *args, **kwargs):  # noqa: ARG002
        """Add members to collection."""
        try:
            members = json.loads(request.data['qset'])
            obj = self.get_object()

            new_members = []
            for member in members:
                record = Record.objects.get(pk=member)
                if not CollectionMembership.objects.filter(collection_id=obj.id, object_id=record.id).exists():
                    new_entry = CollectionMembership()
                    new_entry.collection_id = obj
                    new_entry.content_object = record
                    new_members.append(new_entry)

            CollectionMembership.objects.bulk_create(new_members)
            return Response({'message': 'Action succesful.'}, 201)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

    @action(detail=True, methods=['patch'])
    def remove_members(self, request, *args, **kwargs):  # noqa: ARG002
        """Remove members from collection."""
        try:
            collection_id = kwargs.get('pk')
            members = self.request.data['members']
            member_objects = CollectionMembership.objects.filter(collection_id=collection_id, object_id__in=members)
            member_objects.delete()
            return Response({'message': 'Action succesful.'}, 201)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)
