from calendar import month_name

from django import template

from dalme_app.web_serializers import RecordSerializer
from dalme_public.models import (
    Essay, FeaturedObject, FeaturedInventory, Features, Footer, Home
)


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
    inventories = context.get('inventories')
    inventory = context.get('inventory')
    if inventories or inventory:
        corpus = page.get_parent()
        breadcrumbs[-1].update({'active': False})
        breadcrumbs = [
            *breadcrumbs,
            {
                'title': 'Inventories',
                'url': f'{page.url}inventories/?corpus={corpus.pk}&collection={page.pk}',  # noqa
                'active': True if inventories else False,
            },
        ]

    if inventory:
        title = context['data']['short_name']
        url = page.url + f'inventories/{context["data"]["id"]}/'
        breadcrumbs = [
            *breadcrumbs,
            {'title': title, 'url': url, 'active': True},
        ]

    return breadcrumbs


@register.simple_tag(takes_context=True)
def get_flat_nav(context):
    return [page.specific for page in context['page'].get_siblings().live()]


@register.simple_tag
def get_object_nav():
    return reversed(FeaturedObject.objects.all().order_by(
        '-first_published_at'
    )[:3])


@register.simple_tag
def get_inventory_nav():
    return reversed(FeaturedInventory.objects.all().order_by(
        '-first_published_at'
    )[:3])


@register.simple_tag
def get_header_image_styles(header_image):
    colour = 'rgba(59, 103, 130, 0.6)'
    gradient = f'linear-gradient({colour}, {colour})'
    background = f'{gradient}, url({header_image.url})'
    return f'background: {background}; background-size: cover;'


@register.simple_tag(takes_context=True)
def get_source_details(context):
    page = context['page']
    source = page.source
    source_set = page.source_set

    if source:
        data = RecordSerializer(source).data
        name = data['name']
        short_name = data['short_name']
        date = data['date']
        city = data['city']

    url = None
    if source and source_set:
        stem = 'public/DALME/corpora'
        collection = source_set.public_collections.first()
        url = f'/{stem}/{collection.slug}/inventories/{source.pk}'

    return {
        'source': source,
        'source_set': source_set,
        'name': name,
        'short_name': short_name,
        'date': date,
        'city': city,
        'url': url,
    }


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


@register.simple_tag()
def get_recent_objects():
    objs = reversed(
        FeaturedObject.objects.live().order_by(
            '-first_published_at'
        )[:3]
    )
    return [
        {'url': obj.url, 'month': month_name[obj.first_published_at.month]}
        for obj in objs
    ]


@register.simple_tag()
def get_recent_inventories():
    objs = reversed(
        FeaturedInventory.objects.live().order_by('-first_published_at')[:3]
    )
    return [
        {'url': obj.url, 'month': month_name[obj.first_published_at.month]}
        for obj in objs
    ]


@register.simple_tag()
def get_recent_essays():
    objs = reversed(Essay.objects.live().order_by('-first_published_at')[:3])
    return [
        {'url': obj.url, 'month': month_name[obj.first_published_at.month]}
        for obj in objs
    ]


@register.simple_tag()
def collection_date_range(collection):
    years = sorted(collection.source_set.get_time_coverage.keys())
    return f'{years[0]} - {years[-1]}'
