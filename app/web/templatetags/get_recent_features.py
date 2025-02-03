"""Templatetag for returning recent features."""

from calendar import month_name

from django import template

from web.models import (
    Essay,
    FeaturedInventory,
    FeaturedObject,
)

register = template.Library()


@register.simple_tag(takes_context=True)
def get_recent_features(context):
    feature_type = context.get('feature_type')
    if feature_type == 'Essay':
        title = 'Essays'
        objs = Essay.objects.live().specific().order_by('-go_live_at')[:24]
    elif feature_type == 'Inventory':
        title = 'Inventories'
        objs = FeaturedInventory.objects.live().specific().order_by('-go_live_at')[:24]
    elif feature_type == 'Object':
        title = 'Objects'
        objs = FeaturedObject.objects.live().specific().order_by('-go_live_at')[:24]
    else:
        return None

    results = {}
    year_control = None
    year_set = []
    m_idx = None
    months = [month_name[i][:3] for i in range(1, 13)]

    for i, obj in enumerate(objs):
        year = obj.go_live_at.strftime('%Y')
        month = month_name[obj.go_live_at.month][:3]

        if i == 0:
            year_control = year
            m_idx = months.index(month) - 1
            year_set.append({'url': obj.url, 'month': month})
            continue

        if year == year_control:
            if month != months[m_idx]:
                while month != months[m_idx]:
                    year_set.append({'url': None, 'month': months[m_idx]})
                    m_idx -= 1

            year_set.append({'url': obj.url, 'month': month})
            m_idx -= 1

        else:
            results[year_control] = year_set
            year_control = year
            year_set = [{'url': obj.url, 'month': month}]
            m_idx = months.index(month) - 1

        results[year_control] = year_set

    if results:
        return {'title': title, 'features': results}

    return None
