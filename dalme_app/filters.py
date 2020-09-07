from django_filters import rest_framework as filters
from dalme_app.models import Source


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
                return parent
            elif mode == 'all':
                return parent.filter(is_private=False)
            else:
                return parent.filter(owner=self.request.user)
        else:
            return parent
