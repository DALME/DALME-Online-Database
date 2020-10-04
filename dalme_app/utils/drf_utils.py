import json
from django.conf import settings
from django.http import QueryDict
from rest_framework import permissions, renderers, parsers
from rest_framework.compat import INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from dynamic_preferences.registries import global_preferences_registry


class DRFSelectRenderer(renderers.JSONRenderer):
    """ Django Rest Framework renderer to return selectize ready value lists """

    format = 'select'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)
        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        select_fields = ['name', 'id']

        global_preferences = global_preferences_registry.manager()
        if renderer_context.get('model') is not None:
            if global_preferences['api_settings__model_select_fields'].get(renderer_context['model']) is not None:
                select_fields = global_preferences['api_settings__model_select_fields'].get(renderer_context['model'])

        select_list = []
        if renderer_context.get('select_type') is not None:
            if renderer_context['select_type'] == 'att':
                for entry in data:
                    select_list.append({
                        select_fields[1]: '{{"class": "{}", "id": "{}"}}'.format(renderer_context['model'], entry[select_fields[1]]),
                        select_fields[0]: entry[select_fields[0]]
                    })
        else:
            for entry in data:
                entry_dict = {}
                for field in select_fields:
                    entry_dict[field] = entry[field]
                select_list.append(entry_dict)

        ret = json.dumps(
            select_list, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )
        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()


class DRFDTEJSONRenderer(renderers.JSONRenderer):
    """ Django Rest Framework renderer that returns Datatables Editor format """

    media_type = 'application/json-dte'
    format = 'json-dte'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        if data.get('fieldErrors') is None:
            data = {'data': data}

        ret = json.dumps(
            data, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )

        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()


class DRFDTEParser(parsers.BaseParser):
    """ Django Rest Framework parser that translates Datatables Editor format """

    media_type = 'application/json-dte'
    renderer_class = DRFDTEJSONRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        parsed_data = QueryDict(stream.read(), encoding=encoding)
        return self.convert_dte_data(parsed_data)

    def convert_dte_data(self, parsed_data):
        (id, dte_data), = json.loads(parsed_data['data'])['data'].items()
        data = {}
        for field, value in dte_data.items():
            if 'many-count' not in field:
                if self.clean_entry(value) is not None:
                    data[field] = self.clean_entry(value)
        return data

    def clean_entry(self, value):
        if type(value) is list:
            if len(value) == 0:
                return False
            if len(value) == 1 and value[0] in [1, '1']:
                return True
            elif len(value) > 0:
                return [self.clean_entry(i) for i in value]
        elif type(value) is dict:
            if len(value) > 0:
                value_dict = {k: self.clean_entry(v) for k, v in value.items() if self.clean_entry(v) is not None and 'many-count' not in k}
                return value_dict if len(value_dict) > 0 else None
        elif type(value) is str:
            if value.isdigit():
                return int(value)
            elif value in ['', 'none', 'null', 'Null']:
                return None
            else:
                return value
        else:
            return value


class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Object-level permission to only allow owners of an object to edit it. """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.owner == request.user or request.user.is_superuser:
            return True
        else:
            return False


def DRFDTE_exception_handler(exc, context):
    if isinstance(exc, PermissionDenied):
        return Response({'detail': exc.detail}, 400)
    if isinstance(exc, ValidationError):
        fieldErrors = []
        errors = exc.detail
        for k, v in errors.items():
            if type(v) is dict:
                for k2, v2 in v.items():
                    field = k+'.'+k2
                    try:
                        fieldErrors.append({'name': field, 'status': str(v2[0])})
                    except KeyError:
                        fieldErrors.append({'name': field, 'status': errors})
            else:
                field = k
                fieldErrors.append({'name': field, 'status': str(v[0])})
        return Response({'fieldErrors': fieldErrors}, 400)
    else:
        return None
