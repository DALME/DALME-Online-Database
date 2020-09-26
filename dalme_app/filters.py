from django_filters import rest_framework as filters
from dalme_app.models import Source, Set, Content_type


class ContenTypeFilter(filters.FilterSet):
    id__lt = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = Content_type
        fields = ['id']


class SourceFilter(filters.FilterSet):
    wf_status = filters.NumberFilter(field_name='workflow__wf_status', lookup_expr='iexact')
    wf_stage = filters.NumberFilter(field_name='workflow__stage', lookup_expr='iexact')
    help_flag = filters.BooleanFilter(field_name='workflow__help_flag')
    is_public = filters.BooleanFilter(field_name='workflow__is_public')

    class Meta:
        model = Source
        fields = ['type', 'type__name', 'name', 'short_name', 'owner',
                  'primary_dataset', 'parent', 'has_inventory', 'is_private']

    @property
    def qs(self):
        parent = super().qs
        # change general qs based on superadmin status
        if self.request.GET.get('mode') is not None:
            mode = self.request.GET['mode']
            if mode == 'group':
                dataset = Set.objects.get(dataset_usergroup=self.request.user.profile.primary_group)
                return parent.filter(primary_dataset=dataset.id)
            elif mode == 'all':
                return parent.filter(is_private=False)
            else:
                return parent.filter(owner=self.request.user)
        else:
            return parent


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
