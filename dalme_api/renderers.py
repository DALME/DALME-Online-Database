import json
from rest_framework import renderers
from rest_framework.compat import INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS


class DBRenderer(renderers.BaseRenderer):
    media_type = 'application/json-dte'
    format = 'db'


class SelectRenderer(renderers.JSONRenderer):
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
                    entry_dict[field] = entry.get(field)
                select_list.append(entry_dict)

        ret = json.dumps(
            select_list, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )
        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()


class DTEJSONRenderer(renderers.JSONRenderer):
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
