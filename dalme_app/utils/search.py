import math
import os
import json
from django.conf import settings
from dalme_app.documents import * # NOQA
from django.utils.functional import cached_property
from elasticsearch_dsl.query import Q
import elasticsearch.exceptions as es_exceptions
from dalme_app.documents import PublicSource, FullSource
from dalme_app.models import Attribute, LanguageReference, Set, Source
from dateutil.parser import parse


class Search():

    def __init__(self, data=None, public=False, page=1, highlight=True, as_queryset=False,
                 fragment_size=150, boundary_max_scan=100, sort=False, order=False, search_context=False):
        self.errors = []
        self.results_per_page = getattr(settings, "SEARCH_RESULTS_PER_PAGE", 10)
        self.searchindex = PublicSource if public else FullSource
        self.adjacent_pages = 2
        self.highlight = highlight
        self.highlight_fields = {}
        self.sort = sort
        self.order = order
        self.as_queryset = as_queryset
        self.fragment_size = fragment_size
        self.boundary_max_scan = boundary_max_scan
        self.to_queryset = []

        if not data:
            self.errors.append('No data included with the request')

        if not search_context:
            self.errors.append('No context data included with the request')

        self.data = data
        self.search_context = search_context['fields']
        self.page = int(page)

        if self.page < 1:
            self.errors.append('Page number should be 1 or greater')
            self.page = 1

        self.paginator, self.results = self.get_results

    @cached_property
    def get_results(self):
        query = self.build_query()
        if not query:
            self.errors.append('No query could be built from the request.')
            return ({}, [])

        sqs = self.searchindex.search().query(query)

        if self.highlight:
            for field, options in self.highlight_fields.items():
                sqs = sqs.highlight(field, **options)

        if self.as_queryset:
            sqs = sqs[:1000].to_queryset()

            if self.order:
                sqs = sqs.order_by(self.order)

            return [], sqs

        if self.sort:
            sqs = sqs.sort(self.sort)

        return self.paginate(sqs, self.page, self.results_per_page, self.adjacent_pages)

    def paginate(self, sqs, page, results_per_page, adjacent_pages):
        try:
            total_count = sqs.count()
            num_pages = math.ceil(total_count / self.results_per_page)
            start_offset = (self.page - 1) * self.results_per_page

            result_end = start_offset + self.results_per_page + 1
            if result_end > total_count:
                result_end = total_count

            start_page = max(self.page - self.adjacent_pages, 1) if max(self.page - self.adjacent_pages, 1) >= 3 else 1
            end_page = self.page + self.adjacent_pages if self.page + self.adjacent_pages <= num_pages else num_pages
            page_numbers = [i for i in range(start_page, end_page + 1)]

            paginator = {
                'total_count': total_count,
                'result_start': start_offset + 1,
                'result_end': result_end,
                'num_pages': num_pages,
                'current_page': self.page,
                'previous_page': self.page - 1,
                'next_page': self.page + 1,
                'page_numbers': page_numbers,
                'show_first': 1 not in page_numbers,
                'show_last': num_pages not in page_numbers,
                'has_previous': self.page > start_page,
                'has_next': self.page < end_page
            }

            sqs = sqs[start_offset:start_offset + self.results_per_page]

            return (paginator, sqs.execute())

        except es_exceptions.ConnectionError as e:
            self.errors.append(f'There was an error connecting to the search index: {e.info}')
            return ({}, [])

        except es_exceptions.RequestError as e:
            if e.error == 'parsing_exception':
                self.errors.append(f'There was an error parsing your query: {e.info}')
            else:
                self.errors.append(f'Error ({e.error}): {e.info["error"]["reason"]}')
            return ({}, [])

    def build_query(self):
        data = self.clean_data(self.data, self.search_context)
        if data is None:
            return False

        bool_sets = {'must': [], 'should': [], 'must_not': []}
        for row in data:
            join = row.get('join_type', False)
            method = getattr(self, row.get('field_type'), False)

            if method:
                query, highlight, error = method(row)
                if join and query:
                    bool_sets[join].append(query)

                if highlight:
                    self.highlight_fields.update(highlight)

                if error:
                    self.errors.append(error)

        if bool_sets['must'] or bool_sets['should'] or bool_sets['must_not']:
            query_object = {}

            if bool_sets['must']:
                query_object['must'] = bool_sets['must']

            if bool_sets['should']:
                query_object['should'] = bool_sets['should']

            if bool_sets['must_not']:
                query_object['must_not'] = bool_sets['must_not']

                if not bool_sets['must']:
                    query_object['must'] = [Q('term', type=13)]  # prevents search from returning single folios as results

            return Q('bool', **query_object)

        return False

    @staticmethod
    def clean_data(data, context):
        clean_data = []
        falsy = [None, '', ' ', 'none', False, 'null']
        for i, row in enumerate(data):
            if not row:
                data.pop(i)
            elif row.get('field_value') in falsy and row.get('query') in falsy:
                data.pop(i)

        if len(data) == 1 and data[0]['field_value'] == '':
            querystring = data[0]['query'].strip()
            has_digits = any(char.isdigit() for char in querystring)
            if has_digits:
                try:
                    querystring = parse(querystring).strftime('%Y-%m-%d')
                    fields = [field for field, props in context.items() if props['type'] == 'date']
                    for field in fields:
                        clean_data.append({
                            'field': field,
                            'field_type': context[field]['type'],
                            'field_value': querystring,
                            'query_type': False,
                            'join_type': 'or',
                            'range_type': 'value',
                            'child_relationship': False,
                            'highlight': context[field].get('highlight', {})
                        })
                except ValueError:
                    pass

            for field, props in context.items():
                if props['type'] != 'date':
                    clean_data.append({
                        'field': field,
                        'field_type': context[field]['type'],
                        'field_value': querystring,
                        'query_type': 'match_phrase',
                        'join_type': 'or',
                        'range_type': False,
                        'child_relationship': context[field].get('child_relationship', False),
                        'highlight': context[field].get('highlight', {})
                    })
        else:
            for row in data:
                clean_data.append({
                    'field': row['field'],
                    'field_type': context[row['field']]['type'],
                    'field_value': row['field_value'],
                    'query_type': row['query_type'],
                    'join_type': row['join_type'],
                    'range_type': row['range_type'],
                    'child_relationship': context[row['field']].get('child_relationship', False),
                    'highlight': context[row['field']].get('highlight', {})
                })

        return clean_data if clean_data else None

    @staticmethod
    def date(data):
        try:
            query_date = parse(data['field_value'].strip()).strftime('%Y-%m-%d')
            query_object = {
                data['range_type']: query_date
            }
            query = 'term' if data['range_type'] == 'value' else 'range'
            query = Q(query, **{data['field']: query_object})
            highlight = {data['field']: data['highlight']} if data.get('highlight', False) else False

            return query, highlight, False

        except ValueError:
            errors = [(
                'Value "{}" could not be parsed into a date for field "{}". \
                Try reformatting it, for example as "DD-MM-YYYY"'.format(data['field_value'], data['field'])
            )]
            return False, False, errors

    @staticmethod
    def keyword(data):
        query_object = {'value': data['field_value']}
        query = Q('term', **{data['field']: query_object})
        highlight = {data['field']: data['highlight']} if data.get('highlight', False) else False

        return query, highlight, False

    @staticmethod
    def text(data):
        querystring = data['field_value'].strip()
        query = 'match_phrase_prefix' if data['query_type'] == 'prefix' and ' ' in querystring else data['query_type']
        field = f'{data["field"]}.keyword' if query == 'term' else data['field']
        keyname = 'value' if query in ['term', 'prefix'] else 'query'
        query_object = {keyname: querystring}
        if query == 'match':
            query_object.update({
                'query': querystring,
                'lenient': True,
                'operator': 'OR',
                'fuzziness': 'AUTO',
                'max_expansions': 10,
                'prefix_length': 2,
            })

        query = Q({query: {field: query_object}})
        highlight = {field: data['highlight']} if data.get('highlight', False) else False

        if data.get('child_relationship', False):

            child_object = {
                'type': data['child_relationship'],
                'query': query,
                'inner_hits': {}
            }

            if data.get('highlight', False):
                highlight = data['highlight']
                highlight.update({
                    'fields': {field: {}}
                })
                child_object.update({
                    'inner_hits': {
                        'highlight': highlight
                    }
                })

            query = Q({'has_child': child_object})
            highlight = False

        return query, highlight, False


class SearchContext():

    def __init__(self, **kwargs):
        self.public = kwargs.pop('public', False)

    @cached_property
    def fields(self):
        return [(field, props['label']) for field, props in self.context['fields'].items()]

    @cached_property
    def context(self):
        filename = 'public_source.json' if self.public else 'full_source.json'
        with open(os.path.join('dalme_app', 'config', 'search', filename), 'r') as fp:
            field_data = json.load(fp)

        for field, props in field_data.items():
            if props['type'] == 'keyword':
                props['options'] = self.get_options(field)

        session_var = 'public-search-post' if self.public else 'search-post'

        return {
            'session_var': session_var,
            'fields': field_data
        }

    def get_options(self, field):
        if '.' in field:
            field_tokens = field.split('.')
            field = field_tokens[0] if field_tokens[0] != 'attributes' else field_tokens[1]
        method = getattr(self, field, 'Invalid field')
        return method()

    def collections(self):
        filter_options = {'set_type': 2}
        if self.public:
            filter_options.update({'is_public': True})
        return [{'value': i, 'label': i}
                for i in Set.objects.filter(**filter_options)
                .order_by('name')
                .values_list('name', flat=True)
                ]

    def language(self):
        filter_options = {'type': 13}
        if self.public:
            filter_options.update({'workflow__is_public': True})
        id_list = list(Attribute.objects.filter(
                    attribute_type__short_name='language',
                    object_id__in=Source.objects.filter(**filter_options).values('id')
                ).values_list('value_JSON__id', flat=True).distinct())
        return [{'value': i.name, 'label': i.name}
                for i in LanguageReference.objects.filter(id__in=id_list)
                .order_by('name')
                ]

    def record_type(self):
        filter_options = {'type': 13}
        if self.public:
            filter_options.update({'workflow__is_public': True})
        return [{'value': i, 'label': i}
                for i in Attribute.objects.filter(
                    attribute_type__short_name='record_type',
                    object_id__in=Source.objects.filter(**filter_options).values('id')
                ).order_by('value_STR').values_list('value_STR', flat=True).distinct()
                ]
