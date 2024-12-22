"""Define search utils."""

import json
import math
import pathlib
from contextlib import suppress

import elasticsearch.exceptions as es_exceptions
from dateutil.parser import parse
from elasticsearch_dsl.query import Q

from django.conf import settings
from django.utils.functional import cached_property

from search.documents import FullRecord, WebRecord
from search.forms import SearchForm


class Search:
    """Search query including ancillary logic."""

    def __init__(  # noqa: PLR0913
        self,
        data=None,
        public=False,
        page=1,
        highlight=True,
        as_queryset=False,
        fragment_size=150,
        boundary_max_scan=100,
        sort=False,
        order=False,
        search_context=False,
    ):
        """Initialize class."""
        self.errors = []
        self.results_per_page = getattr(settings, 'SEARCH_RESULTS_PER_PAGE', 10)
        self.searchindex = WebRecord if public else FullRecord
        self.adjacent_pages = 1
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
        """Perform query."""
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

        return self.paginate(sqs)

    def paginate(self, sqs):
        """Paginate search results."""
        try:
            total_count = sqs.count()
            num_pages = math.ceil(total_count / self.results_per_page)
            start_offset = (self.page - 1) * self.results_per_page
            result_end = start_offset + self.results_per_page + 1
            result_end = total_count if result_end > total_count else result_end
            start_page = max(self.page - self.adjacent_pages, 1)
            start_page = start_page if start_page >= 3 else 1  # noqa: PLR2004
            end_page = self.page + self.adjacent_pages if self.page + self.adjacent_pages <= num_pages else num_pages
            page_numbers = list(range(start_page, end_page + 1))
            sqs = sqs[start_offset : start_offset + self.results_per_page]
            paginator = {
                'total_count': total_count,
                'result_start': start_offset + 1,
                'result_end': result_end - 1 if result_end != total_count else result_end,
                'num_pages': num_pages,
                'current_page': self.page,
                'previous_page': self.page - 1,
                'next_page': self.page + 1,
                'page_numbers': page_numbers,
                'show_first': 1 not in page_numbers,
                'show_last': num_pages not in page_numbers,
                'has_previous': self.page > start_page,
                'has_next': self.page < end_page,
            }

            return (paginator, sqs.execute())

        except es_exceptions.ConnectionError as e:
            self.errors.append(f'There was an error connecting to the search index: {e.info}')
            return ({}, [])

        except es_exceptions.RequestError as e:
            if e.error == 'parsing_exception':
                self.errors.append(f'There was an error parsing your query: {e.info}')
            else:
                self.errors.append(f"Error ({e.error}): {e.info['error']['reason']}")
            return ({}, [])

    @staticmethod
    def get_query_object(bool_sets):
        """Take bool sets and return query object."""
        query_object = {}

        if bool_sets['must']:
            query_object['must'] = bool_sets['must']

        if bool_sets['should']:
            query_object['should'] = bool_sets['should']

        if bool_sets['must_not']:
            query_object['must_not'] = bool_sets['must_not']

            if not bool_sets['must']:
                query_object['must'] = [
                    Q('term', short_name__isnull=False),
                ]  # prevents returning of single folios as results

        return query_object

    @staticmethod
    def get_join(row, data, first=False):
        """Calculate join."""
        join = row.get('join_type', False)
        if first and len(data) > 1:
            join = data[1].get('join_type', False)
            if join and join == 'must_not':
                join = 'must'

        return join

    def get_bool_sets(self, data):
        """Calculate bool sets."""
        bool_sets = {'must': [], 'should': [], 'must_not': []}
        child_rel = False
        child_highlight = False

        for i, row in enumerate(data):
            join = self.get_join(row, data, i == 0)
            method = getattr(self, row.get('field_type'), False)

            if row.get('child_relationship', False):
                if child_rel and child_highlight:
                    row['highlight'] = False

                elif row.get('highlight', False):
                    child_highlight = True

                child_rel = True

            if method:
                query, highlight, error = method(row)
                if join and query:
                    bool_sets[join].append(query)

                if highlight:
                    self.highlight_fields.update(highlight)

                if error:
                    self.errors.append(error)

        return bool_sets

    def build_query(self):
        """Build query."""
        data = self.clean_data(self.data, self.search_context)

        if data is None:
            return False

        bool_sets = self.get_bool_sets(data)
        if bool_sets['must'] or bool_sets['should'] or bool_sets['must_not']:
            return Q('bool', **self.get_query_object(bool_sets))

        return False

    @staticmethod
    def clean_data(data, context):
        """Clean form data."""
        clean_data = []
        falsy = [None, '', ' ', 'none', False, 'null']
        for i, row in enumerate(data):
            if not row or (row.get('field_value') in falsy and row.get('query') in falsy):
                data.pop(i)

        if len(data) == 1 and not data[0]['field_value']:
            querystring = data[0]['query'].strip()
            has_digits = any(char.isdigit() for char in querystring)
            if has_digits:
                with suppress(ValueError):
                    querystring = parse(querystring).strftime('%Y-%m-%d')
                    fields = [field for field, props in context.items() if props['type'] == 'date']
                    for field in fields:
                        clean_data.append(
                            {
                                'field': field,
                                'field_type': context[field]['type'],
                                'field_value': querystring,
                                'query_type': False,
                                'join_type': 'or',
                                'range_type': 'value',
                                'child_relationship': False,
                                'highlight': context[field].get('highlight', {}),
                            },
                        )

            for field, props in context.items():
                if props['type'] != 'date':
                    clean_data.append(
                        {
                            'field': field,
                            'field_type': context[field]['type'],
                            'field_value': querystring,
                            'query_type': 'match_phrase',
                            'join_type': 'should',
                            'range_type': False,
                            'child_relationship': context[field].get('child_relationship', False),
                            'highlight': context[field].get('highlight', {}),
                        },
                    )
        else:
            for row in data:
                clean_data.append(
                    {
                        'field': row['field'],
                        'field_type': context[row['field']]['type'],
                        'field_value': row['field_value'],
                        'query_type': row['query_type'],
                        'join_type': row['join_type'],
                        'range_type': row['range_type'],
                        'child_relationship': context[row['field']].get('child_relationship', False),
                        'highlight': context[row['field']].get('highlight', {}),
                    },
                )

        return clean_data if clean_data else None

    @staticmethod
    def date(data):
        """Process date-type data."""
        try:
            query_date = parse(data['field_value'].strip()).strftime('%Y-%m-%d')
            query_object = {data['range_type']: query_date}
            query = 'term' if data['range_type'] == 'value' else 'range'
            query = Q(query, **{data['field']: query_object})
            highlight = {data['field']: data['highlight']} if data.get('highlight', False) else False
            errors = False

        except ValueError:
            query, highlight = False, False
            errors = [
                f'Value "{data["field_value"]}" could not be parsed into a date for field "{data["field"]}". \
                Try reformatting it, for example as "DD-MM-YYYY"',
            ]

        else:
            return query, highlight, errors

    @staticmethod
    def keyword(data):
        """Process keyword-type data."""
        query_object = {'value': data['field_value']}
        query = Q('term', **{data['field']: query_object})
        highlight = {data['field']: data['highlight']} if data.get('highlight', False) else False

        return query, highlight, False

    @staticmethod
    def text(data):
        """Process text-type data."""
        querystring = data['field_value'].strip()
        query = 'match_phrase_prefix' if data['query_type'] == 'prefix' and ' ' in querystring else data['query_type']
        field = f"{data['field']}.keyword" if query == 'term' else data['field']
        keyname = 'value' if query in ['term', 'prefix'] else 'query'
        query_object = {keyname: querystring}

        if query == 'match':
            query_object.update(
                {
                    'query': querystring,
                    'lenient': True,
                    'operator': 'OR',
                    'fuzziness': 'AUTO',
                    'max_expansions': 10,
                    'prefix_length': 2,
                },
            )

        query = Q({query: {field: query_object}})
        highlight = {field: data['highlight']} if data.get('highlight', False) else False

        if data.get('child_relationship', False):
            child_object = {'type': data['child_relationship'], 'query': query}

            if data.get('highlight', False):
                highlight = data['highlight']
                highlight.update({'fields': {field: {}}})
                child_object.update({'inner_hits': {'highlight': highlight}})

            query = Q({'has_child': child_object})
            highlight = False

        return query, highlight, False


class SearchContext:
    """Search context manager."""

    def __init__(self, **kwargs):
        self.public = kwargs.pop('public', False)

    @cached_property
    def fields(self):
        """Return list of field, label tuples."""
        return [(field, props['label']) for field, props in self.context['fields'].items()]

    @cached_property
    def context(self):
        """Return context object."""
        filename = 'search_web_record.json' if self.public else 'search_record.json'
        path = pathlib.Path(f'{settings.PROJECT_ROOT}/app/static/snippets') / filename
        with path.open() as fp:
            field_data = json.load(fp)

        for field, props in field_data.items():
            if props['type'] == 'keyword':
                props['options'] = self.get_options(field)

        session_var = 'web-search-post' if self.public else 'search-post'

        options = {
            'join_types': [{'value': i[0], 'text': i[1]} for i in SearchForm.JOIN_TYPES],
            'query_types': [{'value': i[0], 'text': i[1]} for i in SearchForm.QUERY_TYPES],
            'range_types': [{'value': i[0], 'text': i[1]} for i in SearchForm.RANGE_TYPES],
        }

        return {
            'session_var': session_var,
            'fields': field_data,
            'options': options,
        }

    def get_options(self, field):
        """Return options for keyword fields."""
        if '.' in field:
            field_tokens = field.split('.')
            field = field_tokens[0] if field_tokens[0] != 'attributes' else field_tokens[1]

        method = getattr(self, field, 'Invalid field')
        return method()

    def collections(self):
        """Return collections as options."""
        from domain.models import Collection

        filter_options = {}

        if self.public:
            filter_options.update({'is_published': True})

        return [
            {'value': i, 'text': i}
            for i in Collection.objects.filter(**filter_options).order_by('name').values_list('name', flat=True)
        ]

    def language(self):
        """Return languages as options."""
        from domain.models import Attribute

        filter_options = {'attribute_type__name': 'language'}
        if self.public:
            filter_options.update({'domain_record_related__workflow__is_public': True})

        return [
            {'value': i, 'text': i}
            for i in Attribute.objects.filter(**filter_options)
            .distinct()
            .order_by('value__name')
            .values_list('value__name', flat=True)
        ]

    def record_type(self):
        """Return record types as options."""
        from domain.models import Attribute

        filter_options = {'attribute_type__name': 'record_type'}

        if self.public:
            filter_options.update({'domain_record_related__workflow__is_public': True})

        qs = Attribute.objects.filter(**filter_options).order_by('value__parent__name', 'value__name').distinct()
        return [{'value': i.id, 'text': i.label} for i in qs]
