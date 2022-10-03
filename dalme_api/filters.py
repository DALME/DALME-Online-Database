from django.contrib.auth.models import User
from django_filters import rest_framework as filters

from dalme_app.models import Content_type, RightsPolicy, Source, Set, Task, Ticket


class ContentTypeFilter(filters.FilterSet):
    id__lt = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = Content_type
        fields = ['id']


class SourceFilter(filters.FilterSet):
    wf_status = filters.NumberFilter(field_name='workflow__wf_status', lookup_expr='iexact')
    wf_stage = filters.NumberFilter(field_name='workflow__stage', lookup_expr='iexact')
    help_flag = filters.BooleanFilter(field_name='workflow__help_flag')
    is_public = filters.BooleanFilter(field_name='workflow__is_public')
    ingestion_done = filters.BooleanFilter(field_name='workflow__ingestion_done')
    transcription_done = filters.BooleanFilter(field_name='workflow__transcription_done')
    markup_done = filters.BooleanFilter(field_name='workflow__markup_done')
    review_done = filters.BooleanFilter(field_name='workflow__review_done')
    parsing_done = filters.BooleanFilter(field_name='workflow__parsing_done')
    type__in = filters.NumberFilter(field_name='type', lookup_expr='in')
    type__lt = filters.NumberFilter(field_name='type', lookup_expr='lt')
    pd_null = filters.BooleanFilter(field_name='primary_dataset', lookup_expr='isnull')

    class Meta:
        model = Source
        fields = ['type', 'type__name', 'type__in', 'name', 'short_name', 'owner',
                  'primary_dataset', 'parent', 'has_inventory', 'is_private']

    @property
    def qs(self):
        parent = super().qs
        mode = self.request.GET['mode'] if self.request.GET.get('mode') is not None else 'all'

        if mode == 'team':
            rec_ids = Set.objects.get(dataset_usergroup=self.request.user.profile.primary_group).members.values_list('object_id', flat=True)
            return Source.objects.filter(id__in=rec_ids)

        elif mode == 'all':
            return parent.filter(is_private=False)

        else:
            return parent.filter(owner=self.request.user)


class RightsPolicyFilter(filters.FilterSet):

    class Meta:
        model = RightsPolicy
        fields = ['id', 'name', 'rights_holder', 'rights_status', 'rights', 'public_display',
                  'notice_display', 'licence', 'creation_timestamp',
                  'creation_user', 'modification_user', 'modification_timestamp']


class SetFilter(filters.FilterSet):

    class Meta:
        model = Set
        fields = ['set_type', 'name', 'is_public', 'has_landing', 'endpoint',
                  'permissions', 'description', 'dataset_usergroup', 'dataset_usergroup__name']

    @property
    def qs(self):
        parent = super().qs
        # change general qs based on superadmin status
        if self.request.GET.get('mode') is not None:
            mode = self.request.GET['mode']
            if mode == 'group':
                return parent
            elif mode == 'all':
                return parent.filter(set_type=4)
            else:
                return parent.filter(owner=self.request.user)
        else:
            return parent


class TaskFilter(filters.FilterSet):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'url', 'file',
                  'creation_user', 'creation_timestamp', 'assigned_to']


class TicketFilter(filters.FilterSet):
    # tags = filters.CharFilter(field_name='tags__tag', lookup_expr='icontains')

    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'status', 'url', 'file',
                  'creation_user', 'creation_timestamp', 'assigned_to']


class UserFilter(filters.FilterSet):
    groups = filters.CharFilter(label='groups', method='check_groups')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'profile__full_name', 'groups']

    def check_groups(self, queryset, name, value):
        if ',' in value:
            request_groups = value.split(',')
        else:
            request_groups = [value]

        qs = queryset.none()
        for group in request_groups:
            qs = qs | queryset.filter(groups__name=group)
        return qs.distinct()
