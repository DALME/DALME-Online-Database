"""Templatetag to return citation data."""

import json
import os
import urllib
from datetime import datetime

from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag(takes_context=True)
def get_citation_data(context):  # noqa: C901, PLR0912
    today = datetime.now(tz=timezone.get_current_timezone()).date()
    accessed = today
    page = context['page']
    published = page.first_published_at or today
    page_class = page.get_verbose_name()
    formats = None
    record = context.get('record', False)

    with open(
        os.path.join('public', 'static', 'common', 'citation_styles', 'citation_formats.json'), encoding='utf-8'
    ) as fp:
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
            {'family': 'Morreale', 'given': 'Laura'},
        ],
        'accessed': {'date-parts': [[accessed.year, accessed.month, accessed.day]]},
    }

    if page_class == 'Collections' and not record:
        coins_list += [('rft.genre', 'book'), ('rft.identifier', 'https://dalme.org')]
        citation.update(
            {
                'type': 'book',
                'title': 'The Documentary Archaeology of Late Medieval Europe',
                'URL': 'https://dalme.org',
                'issued': {'date-parts': [[published.year]]},
            },
        )
    else:
        coins_list.append(('rft.genre', 'bookitem'))
        citation.update(
            {
                'type': 'chapter',
                'container-title': 'The Documentary Archaeology of Late Medieval Europe',
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
                ('rft.au', page.record_collection.owner.profile.full_name),
            ]

            citation.update(
                {
                    'author': [{'literal': page.record_collection.owner.profile.full_name}],
                    'issued': {'date-parts': [[published.year]]},
                    'title': page.title,
                    'URL': page.get_full_url(context['request']),
                },
            )

        else:
            author = page.alternate_author if page.alternate_author is not None else page.author
            coins_list += [
                ('rft.atitle', page.title),
                ('rft.identifier', page.get_full_url(context['request'])),
                ('rft.au', author),
            ]

            citation.update(
                {
                    'author': [{'literal': author}],
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
