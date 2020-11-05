import math
from django.conf import settings
from dalme_app.documents import * # NOQA
from elasticsearch_dsl.query import QueryString, Match, Prefix, MatchAll, Bool, Term, Fuzzy, Wildcard
import elasticsearch.exceptions as es_exceptions


def Search(
            data,  # cleaned form data
            searchindex=getattr(settings, "SEARCH_DEFAULT_INDEX", None),  # a search index/document as defined in documents.py
            page=1,  # int, which page in the results page set
            results_per_page=getattr(settings, "SEARCH_RESULTS_PER_PAGE", 10),  # number of results per page
            highlight=False,  # boolean
            fragment_size=False,
            sort=False,  # field name to sort by
        ):

    if not data or searchindex is None:
        return []

    if type(searchindex) is str:
        searchindex = eval(f'{searchindex}()')

    query, highlight_fields = build_query(data)

    sqs = searchindex.search().query(query)

    if highlight:
        sqs = sqs.highlight(*highlight_fields, fragment_size or 100)

    if sort:
        sqs = sqs.sort(sort)

    return paginate(sqs, page, results_per_page)


def build_query(data):
    full_query = MatchAll()
    text_fields = ['name', 'text', 'description', 'locations']
    keyword_fields = ['source_type']
    bool_sets = {
        'and': [],
        'or': []
    }
    highlight_fields = []

    for i, row in enumerate(data):
        if row:
            if row['q'] != '':
                bool_sets['and'].append(Match(
                    text={
                        'query': row['q'].lower().strip(),
                        'operator': 'AND'
                    }))
                highlight_fields.append('text')

            if row['field'] != '':
                if row['field'] in text_fields:
                    highlight_fields.append(row['field'])
                    query_object = {
                        'query': row['field_value'].lower().strip(),
                        'default_field': row['field'],
                        'default_operator': 'AND'
                    }

                    if row['match_type'] == 'exact':
                        query_object.update({
                            'analyzer': 'whitespace',
                            'fuzziness': 0,
                        })

                    if row['match_type'] == 'fuzzy':
                        query_object.update({
                            'fuzziness': 'AUTO',
                            'fuzzy_transpositions': True,
                            'lenient': True
                        })

                    if row['match_type'] == 'prefix':
                        query_tokens = row['field_value'].lower().strip().split(' ')
                        query_object.update({
                            'fuzziness': 'AUTO',
                            'fuzzy_transpositions': False,
                            'fuzzy_prefix_length': len(query_tokens[-1])
                        })

                    if row['wildcards']:
                        query_object.update({
                            'analyze_wildcard': row['wildcards'],
                            'allow_leading_wildcard': False
                        })

                    query = QueryString(**query_object)

                if row['field'] in keyword_fields:
                    highlight_fields.append(row['field'])
                    query_object = {
                        'value': row['field_value'].strip()
                    }

                    if row['match_type'] == 'fuzzy':
                        query_object.update({
                            'fuzziness': 'AUTO',
                            'transpositions': True
                        })
                        query_paras = {row['field']: query_object}
                        query = Fuzzy(**query_paras)

                    else:
                        query_paras = {row['field']: query_object}

                        if row['match_type'] == 'exact':
                            query = Term(**query_paras)

                        elif row['match_type'] == 'prefix':
                            query = Prefix(**query_paras)

                        elif row['wildcards']:
                            query = Wildcard(**query_paras)

                bool_sets[data[i]['operator']].append(query)

    full_query = Bool(
        must=bool_sets['and'],
        should=bool_sets['or']
    )

    highlight_fields = list(set(highlight_fields))
    return full_query, highlight_fields


def paginate(search_obj, page, results_per_page, adjacent_pages=2):
    try:
        page = int(page)
    except (TypeError, ValueError):
        return 'Not a valid number for page.'

    if page < 1:
        return 'Pages should be 1 or greater.'

    try:
        total_count = search_obj.count()
        num_pages = math.ceil(total_count / results_per_page)
        start_offset = (page - 1) * results_per_page

        result_end = start_offset + results_per_page + 1
        if result_end > total_count:
            result_end = total_count

        start_page = max(page - adjacent_pages, 1) if max(page - adjacent_pages, 1) >= 3 else 1
        end_page = page + adjacent_pages if page + adjacent_pages <= num_pages else num_pages
        page_numbers = [i for i in range(start_page, end_page + 1)]

        paginator = {
            'total_count': total_count,
            'result_start': start_offset + 1,
            'result_end': result_end,
            'num_pages': num_pages,
            'current_page': page,
            'previous_page': page - 1,
            'next_page': page + 1,
            'page_numbers': page_numbers,
            'show_first': 1 not in page_numbers,
            'show_last': num_pages not in page_numbers,
            'has_previous': page > start_page,
            'has_next': page < end_page
        }

        search_obj = search_obj[start_offset:start_offset + results_per_page]

        return (paginator, search_obj.execute())

    except es_exceptions.ConnectionError as e:
        return f'There was an error connecting to the search index: {e.info}'

    except es_exceptions.RequestError as e:
        if e.error == 'parsing_exception':
            return 'There was an error parsing your query.'
        else:
            return f'Error ({e.error}): {e.info["error"]["reason"]}'
