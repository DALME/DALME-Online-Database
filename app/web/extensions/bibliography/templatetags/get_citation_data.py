"""Templatetag to return citation data."""

import json
import os
import urllib
from datetime import datetime

from django import template
from django.utils import timezone

from web.models.settings import Settings

register = template.Library()


@register.simple_tag(takes_context=True)
def get_citation_data(context):  # noqa: C901, PLR0912, PLR0915
    today = datetime.now(tz=timezone.get_current_timezone()).date()
    accessed = today
    page = context['page']
    published = page.first_published_at or today
    page_class = page.get_verbose_name()
    formats = None
    record = context.get('record', False)
    settings = Settings.objects.first()

    with open(
        os.path.join('web', 'static', 'common', 'citation_styles', 'citation_formats.json'), encoding='utf-8'
    ) as fp:
        formats = json.load(fp)

    coins_list = [
        ('url_ver', 'Z39.88-2004'),
        ('ctx_ver', 'Z39.88-2004'),
        ('rft_val_fmt', 'info:ofi/fmt:kev:mtx:book'),
        ('rft.btitle', settings.publication_title),
        ('rft.date', f'{published.year}/{published.month}/{published.day}'),
    ]

    editor_names = []
    for editor in settings.editors.all():
        coins_list.append(('rft.au', editor.full_name))
        editor_names.append(
            {
                'family': editor.last_name,
                'given': editor.first_name,
            }
        )

    if settings.doi_handle:
        coins_list.append(('rft.identifier', f'info:doi/{settings.doi_handle}'))

    citation = {
        'editor': editor_names,
        'accessed': {'date-parts': [[accessed.year, accessed.month, accessed.day]]},
    }

    if page_class == 'Collections' and not record:
        coins_list += [
            ('rft.genre', 'book'),
            ('rft.identifier', settings.publication_url),
        ]
        citation.update(
            {
                'type': 'book',
                'title': settings.publication_title,
                'URL': settings.publication_url,
                'issued': {'date-parts': [[published.year]]},
            },
        )
    else:
        coins_list.append(('rft.genre', 'bookitem'))
        citation.update(
            {
                'type': 'chapter',
                'container-title': settings.publication_title,
            },
        )

        if record:
            title = context['data']['name'].strip()
            purl = context['purl']
            authors, corrections, contributors = context['data']['credits']
            contributors = contributors + corrections
            if not authors:
                try:
                    authors = [f"The {context.get('request').tenant.project.name} Team"]
                except:  # noqa: E722
                    authors = 'The IDA Team'
            coins_list += [('rft.atitle', title), ('rft.identifier', purl)]
            for author in authors:
                coins_list.append(('rft.au', author))

            citation.update(
                {
                    'author': [{'literal': i} for i in authors],
                    'title': title,
                    'URL': purl,
                },
            )

            if contributors:
                citation['contributor'] = [{'literal': i} for i in contributors]
                for contributor in contributors:
                    coins_list.append(('rft.contributor', contributor))

        elif page_class == 'Flat':
            coins_list += [('rft.atitle', page.title), ('rft.identifier', page.get_full_url(context['request']))]

            citation.update(
                {
                    'issued': {'date-parts': [[published.year, published.month, published.day]]},
                    'title': page.title,
                    'URL': page.get_full_url(context['request']),
                },
            )

        elif page_class == 'Collection':
            coins_list += [
                ('rft.atitle', page.title),
                ('rft.identifier', page.get_full_url(context['request'])),
                ('rft.au', page.record_collection.owner.full_name),
            ]

            citation.update(
                {
                    'author': [{'literal': page.record_collection.owner.full_name}],
                    'issued': {'date-parts': [[published.year]]},
                    'title': page.title,
                    'URL': page.get_full_url(context['request']),
                },
            )

        else:
            coins_list += [
                ('rft.atitle', page.title),
                ('rft.identifier', page.get_full_url(context['request'])),
                ('rft.au', page.byline),
            ]

            citation.update(
                {
                    'author': [{'literal': page.byline}],
                    'issued': {
                        'date-parts': [
                            [
                                published.year,
                                published.month,
                                published.day,
                            ],
                        ],
                    },
                    'title': page.title,
                    'URL': page.get_full_url(context['request']),
                },
            )
    try:
        coins_tokens = [f'{k}={urllib.parse.quote(v)}' for (k, v) in coins_list]
        coins_span = f'<span class="Z3988" title="{"&".join(coins_tokens)}"></span>'
    except:  # noqa: E722
        return None

    return [formats, citation, coins_span]
