"""Templatetag to return breadcrumbs nav."""

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_breadcrumbs_nav(context):
    page = context['page']
    ancestors = [
        {
            'title': ancestor.specific.title_switch,
            'url': ancestor.specific.url,
            'active': False,
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
                    'active': bool(records),
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
