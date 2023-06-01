from calendar import month_name
import os
import json
import urllib

from django import template
from elasticsearch_dsl.utils import AttrDict

from dalme_public.serializers import PublicSourceSerializer
from dalme_public.models import (
    Essay,
    ExplorePage,
    FeaturedObject,
    FeaturedInventory,
    Features,
    Footer,
    Home,
    SearchPage
)

from datetime import date

register = template.Library()


@register.inclusion_tag(
    'dalme_public/includes/_footer.html', takes_context=True
)
def footer(context):
    return {
        'footer': Footer.objects.first(),
        'year': context['year'],
        'project': context['project'],
    }


@register.filter
def classname(obj):
    return obj.specific.__class__.__name__


@register.simple_tag
def get_nav():
    home = Home.objects.first()
    return [
        page.specific for page in
        (home, *home.get_children().live().filter(show_in_menus=True))
    ]


@register.simple_tag(takes_context=True)
def nav_active(context, tab):
    page = context['page'].specific
    tab = tab.specific
    if page == tab:
        return True
    if not isinstance(tab, Home):
        if page in [desc.specific for desc in tab.get_descendants()]:
            return True
    return False


@register.simple_tag(takes_context=True)
def get_breadcrumbs_nav(context):
    page = context['page']
    ancestors = [
        {
            'title': ancestor.specific.title_switch,
            'url': ancestor.specific.url,
            'active': False
        }
        for ancestor in page.get_ancestors()[1:]
    ]
    current = {'title': page.title_switch, 'url': page.url, 'active': True}
    breadcrumbs = [*ancestors, current]

    # We have to do some contortions here to make sure the RoutablePage
    # endpoints maintain the illusion of being actual Page objects.
    records = context.get('records')
    record = context.get('record')
    search = context.get('search')
    explore = context.get('explore')
    from_search = context.get('from_search')

    if records or record:
        collection = context.get('collection')
        url = f'{page.url}records/'
        if collection:
            url += f'?collection={collection}'
        breadcrumbs[-1].update({'active': False})
        if record and from_search:
            breadcrumbs = [
                *breadcrumbs,
                {
                    'title': 'Search',
                    'url': '/collections/search/',
                    'active': False,
                },
            ]
        else:
            breadcrumbs = [
                *breadcrumbs,
                {
                    'title': 'Browse Records',
                    'url': url,
                    'active': True if records else False,
                },
            ]

    if record:
        title = context['data']['short_name']
        url = page.url + f'records/{context["data"]["id"]}/'
        breadcrumbs = [
            *breadcrumbs,
            {'title': title, 'url': url, 'active': True},
        ]

    if search:
        breadcrumbs[-1].update({'active': False})
        url = f'{page.url}/search/'
        breadcrumbs = [
            *breadcrumbs,
            {'title': 'Search', 'url': url, 'active': True},
        ]

    if explore:
        breadcrumbs[-1].update({'active': False})
        url = f'{page.url}/explore/'
        breadcrumbs = [
            *breadcrumbs,
            {'title': 'Explore', 'url': url, 'active': True},
        ]

    return breadcrumbs


@register.simple_tag(takes_context=True)
def get_flat_nav(context):
    page = context['page']
    if not page.show_in_menus:
        return [p.specific for p in page.get_parent().get_siblings().live().filter(show_in_menus=True)]
    else:
        return [p.specific for p in page.get_siblings().live().filter(show_in_menus=True)]


@register.simple_tag(takes_context=True)
def get_header_image_styles(context, header_image, header_position):
    gradients = {
        'DALME': '125deg, rgba(6, 78, 140, 0.5) 0%, rgba(17, 74, 40, 0.5) 100%',  # noqa
        'project': '125deg, rgba(83, 134, 160, 0.7) 0%, rgba(63, 101, 68, 0.9) 100%',  # noqa
        'features': '125deg, rgba(99, 98, 58, 0.7) 0%, rgba(138, 71, 71, 0.9) 100%',  # noqa
        'collections': '125deg, rgba(95, 81, 111, 0.7) 0%, rgba(23, 62, 101, 0.9) 100%',  # noqa
        'about': '125deg, rgba(105, 102, 63, 0.6) 0%, rgba(146, 106, 16, 0.9) 100%',  # noqa
        'generic': '59deg, #11587c 54.62%, #1b1b1b',
    }
    page = context['page']
    value = False
    count = 0

    while not value and count < 4:
        value = gradients.get(page.slug, False)
        page = page.get_parent()

    if not value:
        value = gradients['generic']

    gradient = f'linear-gradient({value})'
    background_image = f'background-image: {gradient}, url({header_image.url})'
    return f'{background_image}; background-size: cover; background-position-y: {header_position}; width: 100%;'


@register.simple_tag(takes_context=True)
def get_source_details(context):
    page = context['page']
    source = page.source
    source_set = page.source_set
    result = {}

    if source:
        data = PublicSourceSerializer(source).data
        result.update({
            'source': source,
            'name': data['name'],
            'short_name': data['short_name'],
            'date': data.get('date'),
            'locale': data.get('locale'),
            'language': data.get('language'),
            'url': f'/collections/records/{source.pk}/'
        })

    if source_set:
        result.update({
            'source_set': source_set,
            'collection_url': f"/collections/{source_set.name.replace(' ', '-').lower()}/"
        })

    return result if result else None


@register.simple_tag(takes_context=True)
def get_features_filter_q(context, key, value):
    params = f'?{key}={value}' if value != 'all' else ''
    for param_key, param_value in context['request'].GET.items():
        if param_key != key:
            if not params:
                params += f'?{param_key}={param_value}'
            else:
                params += f'&{param_key}={param_value}'
    return params


@register.simple_tag()
def get_features_url():
    return Features.objects.first().url


@register.simple_tag()
def get_features_nav_q(key):
    return {
        'essays': '?kind=essay',
        'inventories': '?kind=inventory',
        'objects': '?kind=object',
    }[key]


@register.simple_tag(takes_context=True)
def get_recent_features(context):
    feature_type = context.get('feature_type')
    if feature_type == 'Essay':
        title = 'Mini Essays'
        objs = Essay.objects.live().specific().order_by('-last_published_at')[:24]
    elif feature_type == 'Inventory':
        title = 'Inventories'
        objs = FeaturedInventory.objects.live().specific().order_by('-last_published_at')[:24]
    elif feature_type == 'Object':
        title = 'Objects'
        objs = FeaturedObject.objects.live().specific().order_by('-last_published_at')[:24]
    else:
        return None

    results = {}
    year_control = None
    year_set = []
    m_idx = None
    months = [month_name[i][:3] for i in range(1, 13)]

    for i, obj in enumerate(objs):
        year = obj.last_published_at.strftime('%Y')
        month = month_name[obj.last_published_at.month][:3]

        if i == 0:
            year_control = year
            m_idx = months.index(month) - 1
            year_set.append({
                'url': obj.url,
                'month': month
            })
            continue

        if year == year_control:
            if month != months[m_idx]:
                while month != months[m_idx]:
                    year_set.append({
                        'url': None,
                        'month': months[m_idx]
                    })
                    m_idx -= 1

            year_set.append({
                'url': obj.url,
                'month': month
            })
            m_idx -= 1

        else:
            results[year_control] = year_set
            year_control = year
            year_set = [{
                'url': obj.url,
                'month': month
            }]
            m_idx = months.index(month) - 1

        results[year_control] = year_set

    if results:
        return {
            'title': title,
            'features': results
        }
    else:
        return None


@register.simple_tag()
def collection_date_range(collection):
    years = sorted(collection.source_set.get_public_time_coverage().keys())
    try:
        return f'{years[0]} - {years[-1]}' if len(years) > 1 else f'{years[0]}+'
    except IndexError:
        return 'Unknown'


@register.simple_tag()
def get_snippet(obj, width):
    return obj.snippet(width)


@register.simple_tag(takes_context=True)
def get_citation_data(context):
    accessed = date.today()
    page = context['page']
    published = page.first_published_at or date.today()
    page_class = page.get_verbose_name()
    formats = None
    record = context.get('record', False)

    with open(os.path.join('static', 'citation_styles', 'citation_formats.json'), 'r', encoding='utf-8') as fp:
        formats = json.load(fp)

    coins_list = [
        ('url_ver', 'Z39.88-2004'),
        ('ctx_ver', 'Z39.88-2004'),
        ('rft_val_fmt', 'info:ofi/fmt:kev:mtx:book'),
        ('rft.au', 'Daniel Lord Smail'),
        ('rft.au', 'Gabriel H. Pizzorno'),
        ('rft.au', 'Laura Morreale'),
        ('rft.btitle', 'The Documentary Archaeology of Late Medieval Europe'),
        ('rft.date', f'{published.year}/{published.month}/{published.day}'),
        # ('rft.identifier', 'info:doi/10.1000/xyz123')
    ]
    citation = {
        'editor': [
            {'family': 'Smail', 'given': 'Daniel Lord'},
            {'family': 'Pizzorno', 'given': 'Gabriel H.'},
            {'family': 'Morreale', 'given': 'Laura'}
        ],
        "accessed": {"date-parts": [[accessed.year, accessed.month, accessed.day]]},
    }

    if page_class == 'Collections' and not record:
        coins_list += [
            ('rft.genre', 'book'),
            ('rft.identifier', 'https://dalme.org'),
        ]
        citation.update({
            'type': 'book',
            'title': 'The Documentary Archaeology of Late Medieval Europe',
            'URL': 'https://dalme.org',
            'issued': {'date-parts': [[published.year]]}
        })
    else:
        coins_list.append(('rft.genre', 'bookitem'))
        citation.update({
            'type': 'chapter',
            'container-title': 'The Documentary Archaeology of Late Medieval Europe',
        })

        if record:
            title = context['data']['name'].strip()
            purl = context['purl']
            authors = context['data']['get_credit_line']['authors']
            contributors = context['data']['get_credit_line']['contributors']

            coins_list += [
                ('rft.atitle', title),
                ('rft.identifier', purl),
            ]
            for author in authors:
                coins_list.append(('rft.au', author))

            citation.update({
                'author': [{'literal': i} for i in authors],
                'title': title,
                'URL': purl
            })

            if contributors:
                citation['contributor'] = [{'literal': i} for i in contributors]
                for contributor in contributors:
                    coins_list.append(('rft.contributor', contributor))

        elif page_class == 'Flat':
            coins_list += [
                ('rft.atitle', page.title),
                ('rft.identifier', page.get_full_url(context['request'])),
            ]

            citation.update({
                'issued': {'date-parts': [[published.year, published.month, published.day]]},
                'title': page.title,
                'URL': page.get_full_url(context['request'])
            })

        elif page_class == 'Collection':
            coins_list += [
                ('rft.atitle', page.title),
                ('rft.identifier', page.get_full_url(context['request'])),
                ('rft.au', page.source_set.owner.profile.full_name),
            ]

            citation.update({
                'author': [{'literal': page.source_set.owner.profile.full_name}],
                'issued': {'date-parts': [[published.year]]},
                'title': page.title,
                'URL': page.get_full_url(context['request'])
            })

        else:
            author = page.alternate_author if page.alternate_author is not None else page.author
            coins_list += [
                ('rft.atitle', page.title),
                ('rft.identifier', page.get_full_url(context['request'])),
                ('rft.au', author)
            ]

            citation.update({
                'author': [{'literal': author}],
                'issued': {'date-parts': [[
                    published.year,
                    published.month,
                    published.day
                ]]},
                'title': page.title,
                'URL': page.get_full_url(context['request'])
            })

    coins_tokens = [f'{k}={urllib.parse.quote(v)}' for (k, v) in coins_list]
    coins_span = f'<span class="Z3988" title="{"&".join(coins_tokens)}"></span>'

    return [formats, citation, coins_span]


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


@register.filter
def dd_record_name(name, part=''):
    try:
        name_string = name.split('(')
        if part == 'loc':

            try:
                return name_string[1][:-1]

            except IndexError:
                return 'Archival location not available'

        return name_string[0]

    except AttributeError:
        return name


@register.simple_tag
def search_help():
    return SearchPage.objects.first()


@register.simple_tag
def explore_map_text():
    return ExplorePage.objects.first()


@register.filter
def to_dict(target):
    if type(target) is AttrDict:
        return target.to_dict()
    if type(target) is list and type(target[0]) is tuple:
        return {i[0]: i[1] for i in target}


@register.simple_tag
def dict_key_lookup(_dict, key):
    return _dict.get(key, '')


@register.filter
def in_list(value, list_string):
    _list = []
    conversions = {
        'none': None,
        'blank': '',
        'empty': ' '
    }

    for item in list_string.split(','):
        if item in conversions:
            _list.append(conversions[item])
        else:
            _list.append(item)

    return value in _list


@register.filter
def get_highlights(meta, context):
    highlights = []
    if 'highlight' in meta:
        fields = list(meta.highlight.to_dict().keys())
        for field in fields:
            for fragment in meta.highlight[field]:
                try:
                    highlights.append({'field': context[field]['label'], 'fragment': fragment})

                except KeyError:
                    field_tokens = field.split('.')
                    field_tokens.pop(-1)
                    highlights.append({'field': context['.'.join(field_tokens)]['label'], 'fragment': fragment})

    if 'inner_hits' in meta:
        docs = list(meta.inner_hits.to_dict().keys())
        for doc in docs:
            for hit in meta.inner_hits[doc].hits:
                if hit.meta:
                    try:
                        fields = hit.meta.highlight.to_dict().keys()
                        for field in fields:
                            for fragment in hit.meta.highlight[field]:
                                highlights.append({'field': f'Folio {hit.folio}',
                                                  'fragment': fragment, 'link': hit.folio})

                    except AttributeError:
                        pass

    return highlights


@register.filter
def js_trans(value, mode=None):
    if mode == 'bool':
        return 'true' if value else 'false'
    elif value is None:
        return 'null'
    elif value is False:
        return 'false'
    elif value is True:
        return 'true'
    elif (type(value) in [int, list, dict]
          or value.startswith('"') and value.endswith('"')
          or value.startswith('\'') and value.endswith('\'')):
        return value
    else:
        return value if value.startswith('"') and value.endswith('"') else f'"{value}"'
