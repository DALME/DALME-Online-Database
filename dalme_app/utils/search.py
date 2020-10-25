import math
from django.conf import settings
from django.http import Http404
from dalme_app.documents import * # NOQA
from elasticsearch_dsl.query import QueryString, MatchPhrasePrefix, MatchBoolPrefix, Match, Prefix


def Search(
            qstring,  # user provided query string - cleaned
            searchindex=getattr(settings, "SEARCH_DEFAULT_INDEX", None),  # a search index/document as defined in documents.py
            load_all=False,  # boolean, True loads all results (no pagination)
            page=1,  # int, which page in the results page set
            results_per_page=getattr(settings, "SEARCH_RESULTS_PER_PAGE", 10),  # number of results per page
            highlight=False,  # tuple, field to highlight + parameters as dict
            sort=False,  # field name to sort by
        ):

    if not qstring or searchindex is None:
        return []

    if type(searchindex) is str:
        searchindex = eval(f'{searchindex}()')

    query = build_query(qstring)
    sqs = searchindex.search().query(query)

    if highlight:
        sqs = sqs.highlight(highlight[0], **highlight[1])

    if sort:
        sqs = sqs.sort(sort)

    if not load_all:
        return paginate(sqs, page, results_per_page)
    else:
        return sqs.execute()


def build_query(qstring):
    if len(qstring.strip().split(' ')) > 1:
        return MatchPhrasePrefix(
            text={'query': qstring},
        )
    else:
        return Prefix(
            text={'value': qstring},
        )


def paginate(search_obj, page, results_per_page, adjacent_pages=2):
    try:
        page = int(page)
    except (TypeError, ValueError):
        raise Http404('Not a valid number for page.')

    if page < 1:
        raise Http404('Pages should be 1 or greater.')

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
