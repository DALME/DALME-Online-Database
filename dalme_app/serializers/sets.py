from dalme_app.models import Set
from rest_framework import serializers
from ._common import DynamicSerializer
import dalme_app.serializers.users as _users
import dalme_app.serializers.others as _others


class SetSerializer(DynamicSerializer):
    owner = _users.UserSerializer(fields=['id', 'full_name', 'username'])
    set_type_name = serializers.CharField(source='get_set_type_display', required=False)
    permissions_name = serializers.CharField(source='get_permissions_display', required=False)
    dataset_usergroup = _others.GroupSerializer()

    class Meta:
        model = Set
        fields = ('id', 'name', 'set_type', 'set_type_name', 'description', 'owner', 'permissions', 'permissions_name', 'workset_progress', 'member_count',
                  'endpoint', 'creation_timestamp', 'is_public', 'has_landing', 'stat_title', 'stat_text', 'dataset_usergroup', 'detail_string')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('workset_progress') is not None and ret.get('set_type') is not None and ret['set_type'] == 4:
            ret['workset'] = '<a class="workset-title" href="/sets/go/{}">{}</a><div class="workset-description">{}</div><div class="workset-endpoint">Endpoint: {}</div>'.format(ret['id'], ret['name'], ret['description'], ret['endpoint'])
            progress = ret['workset_progress']
            angle = round((progress * 360 / 100))
            if angle <= 180:
                right_style = 'style="display:none;"'
                pie_style = ''
            else:
                right_style = 'style="transform:rotate(180deg);"'
                pie_style = 'style="clip:rect(auto, auto, auto, auto);"'
            left_style = 'style="transform:rotate(' + str(angle) + 'deg);"'
            progress_circle = '<div class="pie-wrapper"><span class="label">{}<span class="smaller">%</span></span><div class="pie" {}>'.format(round(progress), pie_style)
            progress_circle += '<div class="left-side half-circle" {}></div><div class="right-side half-circle" {}></div></div></div>'.format(left_style, right_style)
            ret['progress_circle'] = progress_circle
        if ret.get('set_type') is not None:
            ret['set_type'] = {
                'name': ret.pop('set_type_name'),
                'id': ret.pop('set_type')
            }
        if ret.get('permissions') is not None:
            ret['permissions'] = {
                'name': ret.pop('permissions_name'),
                'id': ret.pop('permissions')
            }
        return ret
