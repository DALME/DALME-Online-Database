"""Templatetag for returning sidebar features."""

from calendar import month_name
from datetime import UTC, datetime, timedelta

from django import template

from web.models import (
    Essay,
    FeaturedInventory,
    FeaturedObject,
)

register = template.Library()


@register.simple_tag(takes_context=True)
def get_sidebar_features(context):
    feature_type = context.get('feature_type')
    if feature_type == 'Essay':
        title = 'Essays'
        essays = Essay.objects.live().specific()
        six_months_ago = datetime.now(tz=UTC) - timedelta(days=182)

        return {
            'recent': essays.order_by('-go_live_at')[:5],
            'top_all_time': list(sorted(essays, key=lambda x: x.analytics['visitors'], reverse=True)[:5]),
            'top_six_months': list(
                sorted(
                    essays.filter(go_live_at__gte=six_months_ago), key=lambda x: x.analytics['visitors'], reverse=True
                )[:5]
            ),
        }

    if feature_type in ['Inventory', 'Objects']:
        model = FeaturedInventory if feature_type == 'Inventory' else FeaturedObject
        title = 'Inventories' if feature_type == 'Inventory' else 'Objects'
        objs = model.objects.live().specific().order_by('-go_live_at')[:24]

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
