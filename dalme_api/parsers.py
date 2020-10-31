import json
from django.conf import settings
from django.http import QueryDict
from rest_framework import parsers
from dalme_api.renderers import DTEJSONRenderer


class DTEParser(parsers.BaseParser):
    """ Django Rest Framework parser that translates Datatables Editor format """

    media_type = 'application/json-dte'
    renderer_class = DTEJSONRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        parsed_data = QueryDict(stream.read(), encoding=encoding)
        return self.convert_dte_data(parsed_data)

    def convert_dte_data(self, parsed_data):
        data = {}
        for id, dte_data in json.loads(parsed_data['data'])['data'].items():
            instance_data = {}
            for field, value in dte_data.items():
                if 'many-count' not in field:
                    if self.clean_entry(value) is not None:
                        instance_data[field] = self.clean_entry(value)
            data[id] = instance_data
        return data if len(data) > 1 else data[list(data.keys())[0]]

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
