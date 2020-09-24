import json
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_app.serializers import SetSerializer
from dalme_app.models import Set, Set_x_content, Source
from dalme_app.access_policies import SetAccessPolicy
from dalme_app.filters import SetFilter
from ._common import DALMEBaseViewSet


class Sets(DALMEBaseViewSet):
    """ API endpoint for managing sets """
    permission_classes = (SetAccessPolicy,)
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    filterset_class = SetFilter
    # filterset_fields = ['id', 'name', 'set_type', 'is_public', 'has_landing', 'endpoint', 'permissions', 'dataset_usergroup', 'owner', 'owner__profile__full_name']
    search_fields = ['name', 'endpoint', 'dataset_usergroup__name', 'owner__profile__full_name', 'description']
    ordering_fields = ['name', 'set_type', 'is_public', 'has_landing', 'endpoint', 'permissions', 'dataset_usergroup', 'owner', 'owner__first_name']
    ordering = ['name']

    @action(detail=False, methods=['post'])
    def add_members(self, request, *args, **kwargs):
        result = {}
        try:
            members = json.loads(request.data['qset'])
            object = self.get_object()
            new_members = []
            for i in members:
                source_object = Source.objects.get(pk=i)
                if not Set_x_content.objects.filter(set_id=object.id, object_id=source_object.id).exists():
                    new_entry = Set_x_content()
                    new_entry.set_id = object
                    new_entry.content_object = source_object
                    new_members.append(new_entry)
            Set_x_content.objects.bulk_create(new_members)
            result = {'message': 'Action succesful.'}
            status = 201
        except Exception as e:
            result = {'error': str(e)}
            status = 400
        return Response(result, status)

    @action(detail=True, methods=['patch'])
    def remove_members(self, request, *args, **kwargs):
        try:
            set_id = kwargs.get('pk')
            members = json.loads(self.request.POST['members'])
            member_objects = Set_x_content.objects.filter(set_id=set_id, object_id__in=members)
            member_objects.delete()
            result = {'message': 'Action succesful.'}
            status = 201
        except Exception as e:
            result = {'error': str(e)}
            status = 400
        return Response(result, status)

    @action(detail=True, methods=['patch'])
    def workset_state(self, request, *args, **kwargs):
        try:
            action = self.request.POST['action']
            target = self.request.POST['target']
            set_id = kwargs.get('pk')
            object = Set_x_content.objects.get(set_id=set_id, object_id=target)
            if action == 'mark_done':
                mark = True
            elif action == 'mark_undone':
                mark = False
            object.workset_done = mark
            object.save(update_fields=['workset_done', 'modification_user', 'modification_timestamp'])
            result = {'message': 'Update succesful.'}
            status = 201
        except Exception as e:
            result = {'error': str(e)}
            status = 400
        return Response(result, status)

    # def create(self, request, format=None):
    #     result = {}
    #     data_dict = get_dte_data(request)
    #     data_dict = data_dict[0][1]
    #     if request.data.get('endpoint') is not None:
    #         data_dict['endpoint'] = request.data.get('endpoint')
    #     if request.data.get('qset') is not None:
    #         member_list = json.loads(request.data['qset'])
    #     else:
    #         member_list = None
    #     serializer = self.get_serializer(data=data_dict)
    #     if serializer.is_valid():
    #         new_set = serializer.save()
    #         set_object = Set.objects.get(pk=new_set.id)
    #         if member_list is not None:
    #             new_members = []
    #             for i in member_list:
    #                 source_object = Source.objects.get(pk=i)
    #                 new_entry = Set_x_content()
    #                 new_entry.set_id = set_object
    #                 new_entry.content_object = source_object
    #                 new_members.append(new_entry)
    #             Set_x_content.objects.bulk_create(new_members)
    #         serializer = SetSerializer(set_object)
    #         result = serializer.data
    #         status = 201
    #     else:
    #         result = get_error_array(serializer.errors)
    #         status = 400
    #     return Response(result, status)

    def get_queryset(self, *args, **kwargs):
        search_q = Q()
        if self.request.GET.get('type') is not None:
            type_q = Q(set_type=int(self.request.GET['type']))
            search_q &= type_q
        ownership_q = Q(owner=str(self.request.user.id)) | ~Q(permissions=1)
        search_q &= ownership_q
        queryset = self.queryset.filter(search_q)
        return queryset

    def get_object(self):
        if self.kwargs.get('pk') is not None:
            object = self.queryset.get(pk=self.kwargs.get('pk'))
        else:
            object = self.queryset.get(pk=self.request.data['data[0][set]'])
        return object
